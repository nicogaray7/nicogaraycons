# Research: Shared header and footer

## Decision: delimiter-based region rewrite, not full-page templating

**Decision**: Mark the header and footer with HTML comments
(`<!-- shared:header start -->` / `end`, same for footer) and have the script
replace only the text between those markers. The rest of the file is read and
written back untouched.

**Rationale**: FR-003 requires everything outside the header/footer to stay
byte-identical, and each page has its own unique body, SEO head tags and
sometimes inline scripts. Turning the whole page into a template (one layout file
plus a "content" include) would require re-authoring 35 files end-to-end and
risks losing small per-page differences nobody asked to change. A narrow,
targeted replacement is the smallest change that satisfies FR-003 and FR-009.

**Alternatives considered**:
- *Full-page layout with content includes* (one `layout.html` wrapping a
  per-page body file): rejected, too large a rewrite for a feature scoped to
  header and footer, and it would touch files outside this feature's edges
  (`<head>`, inline page scripts, section markup).
- *Static Site Generator (Eleventy, Hugo, Jekyll)*: rejected. It is a much bigger
  dependency than the problem calls for (no other page content is templated
  today), it would add a build step and a runtime dependency to maintain, and
  GitHub Pages' own Jekyll processing is explicitly disabled by `.nojekyll`
  (Constitution I). Revisit only if a second templating need appears.
- *Client-side include (`fetch` + innerHTML, or a `<script src="header.js">`
  that writes the DOM)*: rejected outright, violates Constitution I (page must
  render fully with JavaScript disabled) and would also delay/flash the header
  and footer on load.

## Decision: Python stdlib script, not a JS build tool

**Decision**: `_shared/render.py`, Python 3.12, no third-party packages.

**Rationale**: The repository has no `package.json`, no `node_modules`, and no
build step today (README: "Static HTML/CSS/JS, no build step or framework").
Python 3.12 is already installed and used elsewhere on the VPS for this project's
tooling (`tools/og`). Adding Node and an npm dependency tree for a ~300-line
substitution script would be a heavier footprint than the problem, and the VPS
has a standing rule to avoid unnecessary heavy installs (`build-guard` exists
because two Next builds once saturated the box). `string.Template` and
`html.parser`/`re` cover placeholder substitution and marker-based extraction
without any dependency.

**Alternatives considered**:
- *Jinja2*: more powerful (loops, conditionals) than needed here; every page's
  variability is already enumerable as a flat key/value settings record (FR-002).
  Would add a pip dependency for a project that currently has zero.
- *Node + a JS templating lib*: rejected for the same reason as a JS build tool
  above, plus it would be the first JS tooling dependency in a project whose
  shipped JS is hand-written and dependency-free.

## Decision: one footer locale, one footer link set per locale (default)

**Decision**: Footer becomes one template per locale (FR, EN) with the same link
set everywhere in that locale, except the per-page tagline and the sibling-city
list, which stay as settings fields.

**Rationale**: The 2026-10-23 measurement showed the footers differ almost only
in `lead=`/`utm_source=` values, the tagline sentence, and which three sibling
cities are linked; the actual link set (Hostinger, Claude until removed, Mercato,
LinkedIn, Malt, legal pages, back-to-top) is otherwise the same everywhere once
those are factored out. Unifying removes exactly the class of drift that caused
PR #86 to require 20 manual edits. Nico confirmed this default over the
alternative (CHOIX reply "Valider, passer au plan").

**Alternatives considered**:
- *Per-page footer link lists*: rejected as the default; it is what produced the
  drift in the first place. Spec's Assumptions section keeps the door open if a
  page genuinely needs a different set later.

## Decision: two header families, not one

**Decision**: Keep `header-home` (used by the generic home pages: `/fr`, `/en`,
city pages, country pages, legal pages) and `header-case` (used by case-study
pages) as two separate templates, each with FR/EN text.

**Rationale**: The diff sample (`fr/index.html` vs `cas/index.html`) shows a
structurally different nav: the home header has in-page section anchors
(`#services`, `#results`, ...) and a language switch with `active`/`aria-current`,
the case-study header has a different class scheme (`cs-nav`) and a single CTA.
Merging them into one shared shape is a redesign, not a dedup, and the spec marks
that out of scope (Assumptions: "The two header families stay distinct").

## Resolved unknowns

No `[NEEDS CLARIFICATION]` markers were left in spec.md; the spec's Assumptions
section already states the defaults taken (footer link set per locale, two
header families, pages without header/footer out of scope). Nothing further to
resolve here.
