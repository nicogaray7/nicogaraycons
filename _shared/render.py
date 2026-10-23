#!/usr/bin/env python3
"""Render the shared header and footer into every page listed under
_shared/pages/*.json.

Usage:
    python3 _shared/render.py            # render and write every page
    python3 _shared/render.py --check    # render in memory, diff, exit 1 on drift

No third-party dependency (stdlib only), see specs/001-shared-header-footer/research.md.
"""
from __future__ import annotations

import json
import string
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SHARED = ROOT / "_shared"
PAGES_DIR = SHARED / "pages"

MARKERS = {
    "header": ("<!-- shared:header start -->", "<!-- shared:header end -->"),
    "footer": ("<!-- shared:footer start -->", "<!-- shared:footer end -->"),
}


class RenderError(Exception):
    pass


SNIPPET_PREFIX = "@snippet:"


def template_path(kind: str, family: str | None, locale: str) -> Path:
    return SHARED / f"{kind}-{family}.{locale}.html"


def resolve_vars(variables: dict, locale: str, page_key: str) -> dict:
    """A var whose value is "@snippet:<name>" is replaced by the content of
    _shared/snippets/<name>.<locale>.html, so text shared by several pages
    (for example the extra footer links of the root and legal pages) lives in
    one file instead of being copied into every page's settings."""
    out = {}
    for key, value in variables.items():
        if isinstance(value, str) and value.startswith(SNIPPET_PREFIX):
            name = value[len(SNIPPET_PREFIX):]
            path = SHARED / "snippets" / f"{name}.{locale}.html"
            if not path.exists():
                raise RenderError(f"{page_key}: missing snippet {path.relative_to(ROOT)}")
            value = path.read_text(encoding="utf-8")
        out[key] = value
    return out


def load_template(kind: str, family: str | None, locale: str) -> string.Template:
    path = template_path(kind, family, locale)
    if not path.exists():
        raise RenderError(f"missing template {path.relative_to(ROOT)}")
    return string.Template(path.read_text(encoding="utf-8"))


def render_region(kind: str, family: str | None, locale: str, variables: dict, page_key: str) -> str:
    tpl = load_template(kind, family, locale)
    try:
        return tpl.substitute(resolve_vars(variables, locale, page_key))
    except KeyError as e:
        raise RenderError(
            f"{page_key}: missing var {e.args[0]!r} for {kind} "
            f"({family or ''} {locale})".strip()
        )


def splice_region(file_text: str, kind: str, new_inner: str, page_key: str) -> str:
    start_marker, end_marker = MARKERS[kind]
    start = file_text.find(start_marker)
    end = file_text.find(end_marker)
    if start == -1 or end == -1:
        raise RenderError(f"{page_key}: no {start_marker} / {end_marker} markers found")
    start_content = start + len(start_marker)
    if end < start_content:
        raise RenderError(f"{page_key}: {kind} end marker before start marker")
    # Keep the indentation of the end marker's line, so indented pages stay
    # byte-identical: templates carry their own leading indentation.
    line_start = file_text.rfind("\n", 0, end) + 1
    indent = file_text[line_start:end]
    if indent.strip():
        indent = ""
    return (file_text[:start_content] + "\n" + new_inner.rstrip("\n") + "\n"
            + indent + file_text[end:])


def load_page_settings() -> list[dict]:
    if not PAGES_DIR.exists():
        return []
    out = []
    for p in sorted(PAGES_DIR.glob("*.json")):
        data = json.loads(p.read_text(encoding="utf-8"))
        data.setdefault("page_key", p.stem)
        out.append(data)
    return out


def render_page(settings: dict) -> tuple[Path, str, list[str]]:
    """Return (file_path, new_text, kinds_rendered) for one page's settings."""
    page_key = settings["page_key"]
    file_path = ROOT / settings["file"]
    if not file_path.exists():
        raise RenderError(f"{page_key}: file not found: {settings['file']}")
    text = file_path.read_text(encoding="utf-8")
    variables = settings.get("vars", {})
    rendered_kinds = []

    header_family = settings.get("header_family")
    header_locale = settings.get("header_locale")
    if header_family and header_locale:
        inner = render_region("header", header_family, header_locale, variables, page_key)
        text = splice_region(text, "header", inner, page_key)
        rendered_kinds.append("header")

    footer_family = settings.get("footer_family")
    footer_locale = settings.get("footer_locale")
    if footer_family and footer_locale:
        inner = render_region("footer", footer_family, footer_locale, variables, page_key)
        text = splice_region(text, "footer", inner, page_key)
        rendered_kinds.append("footer")

    return file_path, text, rendered_kinds


def main() -> int:
    check_only = "--check" in sys.argv[1:]
    pages = load_page_settings()
    if not pages:
        print("no _shared/pages/*.json found, nothing to render")
        return 0

    mismatches: list[str] = []
    errors: list[str] = []
    written = 0

    for settings in pages:
        page_key = settings.get("page_key", "?")
        try:
            file_path, new_text, kinds = render_page(settings)
        except RenderError as e:
            errors.append(str(e))
            continue
        if not kinds:
            continue
        current_text = file_path.read_text(encoding="utf-8")
        if check_only:
            if new_text != current_text:
                mismatches.append(f"{page_key} ({settings['file']})")
        else:
            if new_text != current_text:
                file_path.write_text(new_text, encoding="utf-8")
                written += 1

    if errors:
        for e in errors:
            print(f"ERROR: {e}", file=sys.stderr)
        return 1

    if check_only:
        if mismatches:
            print("Drift detected, these pages no longer match their shared template:")
            for m in mismatches:
                print(f"  - {m}")
            return 1
        print(f"OK: {len(pages)} page(s) match their shared template.")
        return 0

    print(f"Rendered {len(pages)} page(s), {written} file(s) changed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
