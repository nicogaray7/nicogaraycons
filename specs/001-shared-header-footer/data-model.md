# Data Model: Shared header and footer

This feature has no database or runtime data; "entities" below are the build-time
files the render script reads and writes.

## HeaderTemplate

A header source file: `_shared/header-<family>.<locale>.html`.

| Field | Meaning |
|---|---|
| family | `home` or `case` |
| locale | `fr` or `en` |
| body | HTML with `$placeholder` tokens for the per-page values listed under PageSettings |

Constraints:
- Exactly one file per (family, locale) pair that is actually used by a page.
- Every `$placeholder` in the body must have a matching key in every PageSettings
  record that uses this (family, locale).

## FooterTemplate

The footer source file: `_shared/footer-<family>.<locale>.html` (`home` or `case`).

| Field | Meaning |
|---|---|
| locale | `fr` or `en` |
| body | HTML with `$placeholder` tokens, see PageSettings |

Constraints: same as HeaderTemplate, one file per locale actually used.

## PageSettings

One JSON file per page under `_shared/pages/<page-key>.json`.

| Field | Meaning | Example |
|---|---|---|
| page_key | matches the JSON filename, used in error messages | `"lyon"` |
| file | path to the HTML file, relative to repo root | `"lyon/index.html"` |
| header_family | `"home"`, `"case"`, or `null` if the page has no header | `"home"` |
| header_locale | `"fr"` or `"en"` | `"fr"` |
| footer_family | `"home"`, `"case"`, or absent if the page has no shared footer | `"home"` |
| footer_locale | `"fr"` or `"en"` | `"fr"` |
| vars | flat string-to-string map, one entry per placeholder the page's templates need: `lead_footer`, `lead_nav_cta`, `utm_campaign_*`, `tagline`, `nav_logo_href`, `lang_switch_href`, `active_page`, `booking_href`, `sibling_links_html` (pre-rendered `<a>` list for cities), etc. | see quickstart.md |

Validation rules (enforced by `render.py`, not by a schema library, to keep the
zero-dependency constraint):
- `file` must exist.
- If `header_family` is set, `header_locale` must have a matching HeaderTemplate,
  and `vars` must provide every placeholder that template uses.
- Same rule for `footer_locale` and FooterTemplate.
- `render.py --check` additionally asserts that the live region in `file`
  between the `<!-- shared:header -->` / `<!-- shared:footer -->` markers
  equals what rendering would produce, byte for byte.

## Region markers (in existing page files)

Not a new file type, an addition to existing HTML files:

```html
<!-- shared:header start -->
...current header markup, soon replaced by rendered output...
<!-- shared:header end -->
```

and similarly `shared:footer start` / `end`. These markers are the only new
content allowed outside the header/footer's own markup (FR-003).

## Relationships

```
PageSettings.header_family + header_locale  -->  one HeaderTemplate
PageSettings.footer_locale                   -->  one FooterTemplate
PageSettings.file                            -->  one existing HTML page,
                                                    exactly one shared:header
                                                    region and/or one
                                                    shared:footer region
```

A `vars` value of the form `"@snippet:<name>"` is replaced by the content of
`_shared/snippets/<name>.<locale>.html`.

No other state. The render script is stateless between runs; `--check` failures
are reported to stdout/CI, nothing is persisted.
