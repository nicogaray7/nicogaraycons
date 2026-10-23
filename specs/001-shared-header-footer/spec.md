# Feature Specification: Shared header and footer

**Feature Branch**: `shared-header-footer`
**Created**: 2026-10-23
**Status**: Draft
**Input**: User description: "I want the header and footer of this site to be treated as components reused on every page."

## Context

The site has 35 pages with a header and a footer (home pages per locale and city,
case studies, legal pages). Today each page carries its own hand-copied version.
A measurement on 2026-10-23 found 35 distinct headers and 23 distinct footers,
even after ignoring the per-page `lead=` and `utm_source=` values. Removing the
Claude footer link on 2026-10-23 meant editing 20 files one by one. Pages without a
header or footer (redirect pages under `/go/`, `/`, `/en/`, the 404, the OG tool)
are out of scope.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Change the footer once (Priority: P1)

Nico asks for a footer change (add, remove or reword a link, change the
copyright line). The change is made in one place and every page that shows the
footer reflects it after one regeneration step.

**Why this priority**: This is the request itself, and the footer is where drift
costs the most: partner links, affiliate attributes and tracking parameters live
there.

**Independent Test**: Change one footer link in the single source, regenerate,
and confirm all pages with a footer now show the new link and nothing else in
their footer changed.

**Acceptance Scenarios**:

1. **Given** the footer source lists the Hostinger link, **When** the link label is
   changed in the source and pages are regenerated, **Then** every page with a
   footer shows the new label and keeps its own `lead=` value.
2. **Given** a link is removed from the footer source, **When** pages are
   regenerated, **Then** no page shows that link any more.

---

### User Story 2 - Change the header once (Priority: P2)

Nico asks for a header change (logo, call-to-action label, language switch,
a navigation entry common to all pages). The change is made in one place and
reaches every page of the same header family.

**Why this priority**: Same benefit as the footer, but headers legitimately vary
more (each home page links to its own sections), so it comes second.

**Independent Test**: Change the call-to-action label in the header source,
regenerate, and confirm every page of that family shows it while each page keeps
its own section links and booking link parameters.

**Acceptance Scenarios**:

1. **Given** the home header family, **When** the CTA label is changed once,
   **Then** every home, city and legal page shows the new label.
2. **Given** a case study page, **When** the case study header source changes,
   **Then** all FR and EN case study pages reflect it and home pages are untouched.

---

### User Story 3 - Drift is caught before it ships (Priority: P3)

Someone (Nico, an agent) edits a header or footer directly inside one page
instead of the shared source. The mismatch is detected before merge.

**Why this priority**: Without it, the 35 copies drift apart again within weeks.

**Independent Test**: Hand-edit the footer of one page, run the check, and see it
fail naming that page; regenerate and see it pass.

**Acceptance Scenarios**:

1. **Given** a page whose footer was edited by hand, **When** the check runs on the
   pull request, **Then** it fails and names the page.

---

### Edge Cases

- A page in a locale (EN) needs translated labels: the shared source must hold one
  text per locale, never machine-mixed languages on a page.
- A city page links to sibling cities and not to itself.
- The active language link and `aria-current` point to the current page.
- Legal pages (mentions légales, cookies, EN legal notice and cookies) use the home
  header family but have no in-page sections to anchor to.
- The hidden `#partenaire` section is page content, not part of the footer, and is
  untouched.
- The per-page footer tagline (for example "Consultant IA Lyon · Création d'agents
  IA sur mesure") is local SEO copy and must survive.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The site MUST have a single source for the footer and a single source
  per header family (home family, case study family), each holding FR and EN text.
- **FR-002**: Each page MUST be able to set its own values for the parts that
  legitimately differ: `lead=` and `utm_*` values, footer tagline, in-page section
  links, language switch target, booking link parameters, sibling city links,
  active page marker.
- **FR-003**: Regenerating MUST rewrite only the header and footer region of each
  page; everything else in the file stays byte-identical.
- **FR-004**: The served pages MUST still contain the full header and footer as
  plain HTML, readable with JavaScript disabled.
- **FR-005**: Every link, attribute and tracking hook present today in headers and
  footers (`data-cta`, `rel="sponsored nofollow noopener"`, `target`, `lead=`,
  `utm_*`, `aria-*`, the footer year span) MUST be present after migration on the
  same page, unless Nico asks to unify it.
- **FR-006**: A check MUST fail when a page's header or footer differs from what
  the shared source would produce, and MUST name the page.
- **FR-007**: The check MUST run automatically on pull requests.
- **FR-008**: A short how-to in the README MUST say where the sources are and the
  one command to regenerate.
- **FR-009**: The migration MUST not change what visitors see, except where the
  current 35 copies disagree for no reason (for example a footer link present on
  Lyon but missing on Paris); each such unification is listed in the pull request.

### Key Entities

- **Header family**: a shared header layout with FR and EN text (home, case study).
- **Footer**: the shared footer layout with FR and EN text.
- **Page settings**: the per-page values injected into the shared layouts.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: A footer link change touches 1 source file plus the regenerated
  pages, done with 1 command, instead of 20 manual edits.
- **SC-002**: After migration, 0 pages differ from what the sources produce (the
  check passes on `main`).
- **SC-003**: GA4 hits and the `/go/` click events still fire on the FR home, one
  city page, one EN page and one case study, observed in a real browser.
- **SC-004**: Screenshots at phone and desktop width show no visual change on those
  same four pages, apart from the listed unifications.

## Assumptions

- Hosting stays GitHub Pages with `.nojekyll`; no server-side includes exist, so the
  sharing happens before publishing, not in the visitor's browser (Constitution I).
- Regenerated pages are committed, so publishing keeps working exactly as today.
- Footer links become the same set on every page of a locale (default), with sibling
  city links as the only per-page list. Nico can ask to keep page-specific links.
- The two header families stay distinct; merging them into one design is a separate
  request.
- Pages without a header or footer are out of scope.
