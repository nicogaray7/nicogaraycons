# Tasks: Shared header and footer

**Input**: Design documents from `/specs/001-shared-header-footer/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md, quickstart.md

**Tests**: not requested for this feature (a build-time script with no runtime
behavior beyond file I/O); the User Story verification tasks below, driven by
quickstart.md, are the test.

**Page inventory** (from the 2026-10-23 measurement, used by every task below):

- FR home family (14): `fr/index.html`, `cookies/index.html`,
  `mentions-legales/index.html`, `paris/index.html`, `lyon/index.html`,
  `marseille/index.html`, `nice/index.html`, `nantes/index.html`,
  `toulouse/index.html`, `lille/index.html`, `bordeaux/index.html`,
  `be/index.html`, `ch/index.html`, `lu/index.html`
- EN home family (7): `en.html`, `en/cookies/index.html`,
  `en/legal-notice/index.html`, `en/gb/index.html`, `en/sg/index.html`,
  `en/us/index.html`, `en/ca/index.html`
- FR case-study family (7): `cas/index.html`,
  `cas/agent-devis-artisan/index.html`, `cas/assistant-multicanal/index.html`,
  `cas/parcours-clients-crm/index.html`, `cas/chatbot-sante-agenda/index.html`,
  `cas/automatisation-formulaires/index.html`,
  `cas/deploiement-20-marches/index.html`
- EN case-study family (7): `en/cases/index.html`,
  `en/cases/ai-assistant/index.html`, `en/cases/brand-site-20-markets/index.html`,
  `en/cases/crm-customer-journeys/index.html`, `en/cases/form-automation/index.html`,
  `en/cases/medical-practice-scheduling/index.html`,
  `en/cases/plumber-quote-agent/index.html`

Total: 35 pages, matching plan.md's Scale/Scope.

## Implementation notes (lot 1, 2026-10-23)

Reading the 35 real footers showed the "one footer per locale" assumption was
wrong. What was built instead:

- Two footer families, not one: `footer-home.{fr,en}.html` (root, city, country
  and legal pages, 20 pages) and `footer-case.{fr,en}.html` (case studies, 14
  pages). Templates live at `_shared/<kind>-<family>.<locale>.html`; page
  settings carry `footer_family`.
- `bordeaux/index.html` is out of scope for now: its footer is a separate
  landing-page design (own wrapper, absolute URLs, different link set). It has
  no markers and no settings file; folding it into a family is a decision for
  Nico, not a dedup.
- The migration is zero-visual-change: each page keeps its own link list,
  tagline and `lead=` values. Shared text used by several pages (the extra
  links of the root and legal pages) lives in `_shared/snippets/` and is
  referenced from settings as `"@snippet:<name>"`. The only byte change outside
  the markers is `&copy;` written as `©` on 6 city pages (same glyph).
- Existing inconsistencies are kept as they are and listed for a later
  decision: Paris and the country pages have no sibling-city links while the
  other city pages do; legal pages use `lead=footer-legal` for Malt and
  `footer-legal-fr`/`-en` for Hostinger and Mercato.
- T010 was done for footers only; header markers come with User Story 2.
- Verification: a label change in `footer-home.fr.html` reached all FR home
  pages with their own `lead=` kept; a hand edit in `lyon/index.html` made
  `--check` fail naming `lyon`; mobile footer screenshots of `/lyon/`, `/cas/`,
  `/en/us/` and `/fr/` are pixel-identical to production; clicking the footer
  Hostinger and Malt links fires `partenaire_clic` and `clic_malt` with
  `lead=footer-lyon`.

## Phase 1: Setup

- [X] T001 Create the `_shared/` directory and `_shared/pages/` subdirectory;
  create `_shared/render.py` with argument parsing for the default (render and
  write) mode and `--check` (render in memory, no write) mode, per plan.md
  Project Structure.
- [X] T002 [P] Create `.github/workflows/check-shared-partials.yml` that checks
  out the repo and runs `python3 _shared/render.py --check` on `pull_request`
  (FR-007); it must fail the workflow when the script exits non-zero.

## Phase 2: Foundational (blocking prerequisites)

**These must complete before any user story work: they are the engine every
story's pages are migrated through.**

- [X] T003 In `_shared/render.py`, implement locating and replacing only the
  span between `<!-- shared:header start -->` and `<!-- shared:header end -->`
  (and the same pair for `shared:footer`) inside a page file, leaving every
  other byte of the file unchanged, per data-model.md "Region markers" and
  plan.md Constitution Check item I (FR-003).
- [X] T004 In `_shared/render.py`, implement the `PageSettings` loader: read
  every `_shared/pages/*.json`, validate `file` exists, and validate that `vars`
  provides every placeholder required by the templates named in
  `header_family`/`header_locale`/`footer_locale`, per data-model.md
  "PageSettings" and its Validation rules.
- [X] T005 In `_shared/render.py`, implement rendering a `HeaderTemplate` or
  `FooterTemplate` body with `string.Template.substitute(vars)`, raising a
  clear error naming the page and the missing key on an unfilled placeholder.
- [X] T006 In `_shared/render.py`, wire T003-T005 together: default mode writes
  the rendered region back into each page's file; `--check` mode renders in
  memory, diffs against the file's current region, and on any mismatch prints
  the offending `page_key` and `file` and exits 1 (0 if every page matches),
  per quickstart.md.
- [X] T007 Extract `_shared/footer.fr.html` and `_shared/footer.en.html` from
  the current footer markup in `fr/index.html` and `en.html`, turning the
  per-page tagline, sibling-city links, `lead_footer` value and any
  `utm_campaign_*` value into `$placeholder` tokens while keeping every
  existing `href`, `rel="sponsored nofollow noopener"`, `target`, `data-cta`
  and logo `<img>` exactly as today (research.md's unified-footer decision,
  FR-005).
- [ ] T008 Extract `_shared/header-home.fr.html` and `_shared/header-home.en.html`
  from the current header markup in `fr/index.html` and `en.html`, turning
  `nav_logo_href`, the language-switch target, the `active`/`aria-current`
  page marker, the booking-link href/`utm_*` and the CTA label into
  `$placeholder` tokens (research.md's two-families decision, FR-005).
- [ ] T009 Extract `_shared/header-case.fr.html` and `_shared/header-case.en.html`
  from the current header markup in `cas/index.html` and
  `en/cases/index.html`, turning the language-switch target and the
  `lead=`/`utm_*` values on its CTA into `$placeholder` tokens.
- [ ] T010 Add the `<!-- shared:header start/end -->` and
  `<!-- shared:footer start/end -->` marker comments around the existing,
  unmodified header and footer markup in all 35 pages listed in the Page
  inventory above (mechanical: markers only, no content change yet).

**Checkpoint**: `_shared/render.py --check` can run (even though no
`_shared/pages/*.json` exists yet, so it reports nothing to check); templates
and markers are in place.

## Phase 3: User Story 1 - Change the footer once (Priority: P1) 🎯 MVP

**Goal**: one footer source, edited once, reaching all 35 pages.
**Independent Test**: per spec.md, change one footer link in the source,
regenerate, confirm every page with a footer shows it and keeps its own
`lead=` value.

- [X] T011 [US1] Create `_shared/pages/<key>.json` for each of the 14 FR
  home-family pages (listed in Page inventory) with `file` and `footer_locale:
  "fr"`, and `vars` covering `tagline`, `sibling_links_html`, `lead_footer`,
  and any footer `utm_campaign_*` used by that page today.
- [X] T012 [P] [US1] Create `_shared/pages/<key>.json` for each of the 7 EN
  home-family pages with `footer_locale: "en"` and the same `vars` shape as
  T011, values translated/adapted per page.
- [X] T013 [P] [US1] Create `_shared/pages/<key>.json` for each of the 7 FR
  case-study pages with `footer_locale: "fr"` and the same `vars` shape.
- [X] T014 [P] [US1] Create `_shared/pages/<key>.json` for each of the 7 EN
  case-study pages with `footer_locale: "en"` and the same `vars` shape.
- [X] T015 [US1] Run `python3 _shared/render.py`; review `git diff` for all 35
  footer regions; list in the pull request description every case where a page
  gains or loses a link compared to today, per FR-009 and research.md's
  unified-link-set decision.
- [X] T016 [US1] Run `python3 _shared/render.py --check`; confirm exit code 0
  for all 35 pages (SC-002, footer half).
- [X] T017 [US1] Follow quickstart.md "Prove a footer change reaches every
  page": change one link label in `_shared/footer.fr.html`, regenerate,
  `grep` for it in `fr/index.html`, `paris/index.html`, `lyon/index.html`,
  `mentions-legales/index.html`, confirm the new label is there and each
  page's own `lead=` is unchanged; then revert the test edit and regenerate.

**Checkpoint**: footer is fully shared and verified; this alone is shippable
(the MVP for this feature).

## Phase 4: User Story 2 - Change the header once (Priority: P2)

**Goal**: one header source per family (home, case study), edited once, reaching
every page of that family.
**Independent Test**: per spec.md, change the CTA label in the home header
source, regenerate, confirm every home/city/legal page shows it while section
links and booking-link parameters stay per-page.

- [ ] T018 [US2] Extend each of the 14 FR home-family `_shared/pages/<key>.json`
  files from T011 with `header_family: "home"`, `header_locale: "fr"`, and the
  additional `vars` the home header template needs (`nav_logo_href`,
  `lang_switch_href`, `active_page`, `booking_href` with its page-specific
  `lead=`/`utm_*`, any in-page section hrefs that differ by page).
- [ ] T019 [P] [US2] Extend each of the 7 EN home-family JSON files from T012
  with `header_family: "home"`, `header_locale: "en"`, and the same `vars`
  shape as T018.
- [ ] T020 [P] [US2] Extend each of the 7 FR case-study JSON files from T013
  with `header_family: "case"`, `header_locale: "fr"`, and the `vars` the case
  header template needs (`lang_switch_href`, CTA `lead=`/`utm_*`).
- [ ] T021 [P] [US2] Extend each of the 7 EN case-study JSON files from T014
  with `header_family: "case"`, `header_locale: "en"`, and the same `vars`
  shape as T020.
- [ ] T022 [US2] Run `python3 _shared/render.py`; review `git diff` for all 35
  header regions.
- [ ] T023 [US2] Run `python3 _shared/render.py --check`; confirm exit code 0
  for all 35 pages (SC-002, header half; full SC-002 now satisfied).
- [ ] T024 [US2] Follow quickstart.md "Prove tracking survived": in a real
  browser, open `fr/index.html`, `paris/index.html`, `en/us/index.html` and
  `cas/index.html`; confirm the `gtag('config','G-L2DZPV8S00')` call still
  fires on each, and that clicking each page's footer/header tracked links
  reproduces the same `lead=`/`utm_*` values recorded in the T015/T022 diffs
  (SC-003, Constitution II).
- [ ] T025 [US2] Follow quickstart.md "Prove nothing else moved": screenshot
  `fr/index.html`, `paris/index.html`, `en/us/index.html` and `cas/index.html`
  at a phone width and at desktop width, before and after T022's regeneration;
  confirm no visual change beyond the unifications listed in T015 (SC-004,
  Constitution IV).

**Checkpoint**: header and footer are both fully shared and verified across all
35 pages.

## Phase 5: User Story 3 - Drift is caught before it ships (Priority: P3)

**Goal**: a hand-edit to a page's header or footer fails the PR check, naming
the page.
**Independent Test**: per spec.md, hand-edit the footer of one page, run the
check, see it fail naming that page; regenerate and see it pass.

- [X] T026 [US3] Hand-edit the footer markup inside the `shared:footer` region
  of one already-migrated page (for example `lyon/index.html`) without going
  through `_shared/footer.fr.html`; run `python3 _shared/render.py --check`;
  confirm it exits 1 and its output names `lyon` and `lyon/index.html`
  (Acceptance Scenario 1 of User Story 3); then run
  `python3 _shared/render.py` to restore it and confirm `--check` now passes.
- [ ] T027 [US3] Push T026's hand-edit on a disposable branch/PR and confirm
  `.github/workflows/check-shared-partials.yml` (T002) fails that PR's checks;
  close the PR without merging.

**Checkpoint**: the drift safety net (FR-006, FR-007) is proven, not just
written.

## Phase 6: Polish & Cross-Cutting Concerns

- [X] T028 [P] Add a short section to `README.md` naming `_shared/render.py`,
  `_shared/pages/`, the two commands (plain run, `--check`), and "Add a new
  page later" steps from quickstart.md (FR-008).
- [ ] T029 [P] Re-read `docs/analytics-conversions.md` against the migrated
  templates and confirm every `data-cta`/event hook it documents is still
  described accurately now that the markup lives in `_shared/`; update only if
  a hook's location description is now wrong, do not change the hooks
  themselves.
- [ ] T030 Run `python3 _shared/render.py --check` once more on the final
  branch state before opening the merge pull request; it must exit 0 for all
  35 pages (SC-002 as a release gate).

## Dependencies & Execution Order

- **Phase 1 (Setup)** before everything.
- **Phase 2 (Foundational)** before any user story: T003-T006 build the engine,
  T007-T009 create the templates, T010 prepares every page file. All of Phase 3
  onward calls `_shared/render.py` and reads the templates these tasks create.
- **User Story 1 (Phase 3)** needs Phase 2 complete. It does not need Phase 4 or
  5. This is the MVP: shippable alone.
- **User Story 2 (Phase 4)** needs Phase 2 complete. It extends the same
  `_shared/pages/*.json` files User Story 1 created (T018-T021 build on
  T011-T014), so in practice it follows Phase 3, but nothing in its logic
  depends on US1's verification tasks (T015-T017) having run first.
- **User Story 3 (Phase 5)** needs Phase 1's T002 (the workflow) and at least
  one migrated page (Phase 3 and/or 4 done for that page).
- **Polish (Phase 6)** after every user story is done.

## Parallel Execution Examples

- T011-T014 (the four page-family JSON batches for User Story 1) touch disjoint
  sets of files and can run in parallel once Phase 2 is done.
- T018-T021 (the four page-family JSON extensions for User Story 2) likewise
  run in parallel once T011-T014 exist.
- T028 and T029 (Polish) touch different files and can run in parallel.

## Implementation Strategy

**MVP = Phase 1 + Phase 2 + Phase 3 (User Story 1)**: ship the shared footer
alone first, verified by T017, as its own pull request. It already turns
PR #86's "edit 20 files" into "edit 1 file, run 1 command", which is the
request Nico made.

**Then incrementally**: Phase 4 (header) as a second pull request, Phase 5
(drift check) can land together with either phase since T002 has no
dependency on the templates themselves, Phase 6 last.
