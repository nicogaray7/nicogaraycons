# Implementation Plan: Shared header and footer

**Branch**: `001-shared-header-footer` | **Date**: 2026-10-23 | **Spec**: [spec.md](./spec.md)

**Input**: Feature specification from `/specs/001-shared-header-footer/spec.md`

## Summary

Extract the header and footer markup of the 35 pages that carry one into a small
set of source templates (one footer, one header per family: home, case study),
each holding FR and EN text. A build-time Python script renders each page's header
and footer region from its template plus a per-page settings record, and rewrites
only that region in the committed HTML file, so the published output is still
plain HTML with nothing changed at request time. The same script runs in
`--check` mode on every pull request and fails, naming the page, if a file's
header or footer no longer matches what the template would produce.

## Technical Context

**Language/Version**: Python 3.12 (already on the VPS, stdlib only, no `pip
install`, no `npm`, nothing added to `requirements`/`package.json` since the repo
has neither).

**Primary Dependencies**: None. `string.Template` (stdlib) covers the
`$placeholder` substitution; `html.parser` (stdlib) locates the header/footer
region by HTML comment markers. No templating engine, no build tool.

**Storage**: Flat files. Templates under `_shared/`, one JSON settings file per
page family under `_shared/pages/`.

**Testing**: A `--check` mode of the same script (render in memory, diff against
the committed file) plus a GitHub Actions workflow that runs it on every PR. No
test framework is introduced for a 300-line script with no runtime behavior beyond
file I/O; `--check` run locally against every page is the test.

**Target Platform**: GitHub Pages (static files served as committed). The
generation script runs on the VPS or in GitHub Actions only, never in the
visitor's browser.

**Project Type**: Static site plus a small build-time CLI script (single project).

**Performance Goals**: N/A (build-time script over 35 files, not a runtime path).

**Constraints**: Output HTML must be byte-identical to today outside the header
and footer region (Constitution I, FR-003). No JavaScript requirement added to
render the header/footer (Constitution I). GA4 tags, `assets/track.js` hooks,
`data-cta`, `lead=`, `utm_*`, `rel="sponsored nofollow noopener"` survive untouched
unless the page settings explicitly change them (Constitution II, FR-005).

**Scale/Scope**: 35 pages with a footer, 35 with a header, across 2 header
families (home, case study) and 2 locales (FR, EN). One repository, no other
services involved.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- **I. Plain static output**: PASS. Generation happens before commit; GitHub
  Pages still serves committed plain HTML. No framework or runtime dependency
  reaches the page.
- **II. Tracking is part of the page**: PASS, conditioned on FR-005: every
  existing tracking attribute in a header/footer must appear in its template and
  in the per-page settings, verified by diff before the templates are extracted,
  and re-verified live in a browser after migration (Phase 1, quickstart.md).
- **III. SEO signals stay intact**: PASS. Canonical/hreflang live in `<head>`,
  outside the header/footer region, unaffected. `rel="sponsored nofollow"` on
  affiliate links is a tracked attribute under FR-005.
- **IV. Mobile first**: applies to the verification step (quickstart.md), not to
  template authoring itself (no new visual design here).
- **V. Small, reviewable changes**: PASS. Migration is one script run producing
  a diff per page, reviewed as one PR per Tasks guidance (one page family at a
  time, see tasks.md).

No violations requiring justification. Complexity Tracking table is empty.

## Project Structure

### Documentation (this feature)

```text
specs/001-shared-header-footer/
├── plan.md              # This file
├── research.md          # Phase 0 output
├── data-model.md        # Phase 1 output
├── quickstart.md         # Phase 1 output
└── tasks.md             # Phase 2 output (/speckit-tasks, not yet created)
```

No `contracts/` directory: the generation script is an internal build tool with
no API or interface exposed to another system (Phase 1, step 2 of the plan
workflow explicitly allows skipping contracts for build scripts).

### Source Code (repository root)

```text
_shared/
├── render.py                   # the one script: render + --check modes
├── header-home.fr.html         # home-family header template (nav, logo, CTA, lang switch)
├── header-home.en.html
├── header-case.fr.html         # case-study-family header template
├── header-case.en.html
├── footer.fr.html               # single footer template
├── footer.en.html
└── pages/
    ├── fr-index.json            # per-page settings (header family, locale, lead=, taglines,
    ├── paris.json                #   sibling city links, active nav item, booking link, ...)
    ├── lyon.json
    ├── ... (one JSON per page that has a header and/or footer)
    └── en-cases-index.json

.github/workflows/
└── check-shared-partials.yml   # runs `python3 _shared/render.py --check` on pull_request

<existing page files: fr/index.html, paris/index.html, cas/index.html, ...>
# unchanged except the header/footer region, now delimited by:
#   <!-- shared:header start -->...<!-- shared:header end -->
#   <!-- shared:footer start -->...<!-- shared:footer end -->
```

**Structure Decision**: Single project, no `src/`/`tests/` split, this is a
static content site. The one new concept is `_shared/` (templates, per-page
settings and the render script) plus one new GitHub Actions workflow. Page files
keep their current paths and all content outside the marked region.

## Complexity Tracking

*No violations, table intentionally empty.*
