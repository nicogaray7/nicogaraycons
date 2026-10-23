# Quickstart: Shared header and footer

Prerequisites: Python 3.12 (stdlib only, nothing to install), a checkout of this
repository on the feature branch.

## Regenerate every page from the shared sources

```sh
cd nicogaraycons
python3 _shared/render.py
git diff --stat
```

Expected outcome: a diff touching only the files listed in
`_shared/pages/*.json`, each only inside its `<!-- shared:header -->` /
`<!-- shared:footer -->` region.

## Check for drift without writing anything (used in CI)

```sh
python3 _shared/render.py --check
```

Expected outcome: exit code 0 and no output when every page matches its
templates; exit code 1 and one line per mismatching page (its `page_key` and
`file`) otherwise. This is the command `.github/workflows/check-shared-partials.yml`
runs on every pull request (FR-006, FR-007, SC-002).

## Prove a footer change reaches every page (User Story 1)

```sh
# edit one link in _shared/footer.fr.html, e.g. the Hostinger label
python3 _shared/render.py
grep -l "Hostinger" fr/index.html paris/index.html lyon/index.html mentions-legales/index.html
```

Expected: the new label appears in all of them, each page's own `lead=` value
(visible with `grep -o 'lead=[a-z-]*'`) is unchanged.

## Prove tracking survived (Constitution II, SC-003)

Open these four pages in a real browser (Playwright or a disposable headless
browser against a local static server, per the bot's GA4 verification rule) after
regenerating:

- `fr/index.html` (home, FR)
- `paris/index.html` (city)
- `en/us/index.html` (EN)
- `cas/index.html` (case study)

For each: confirm the `gtag('config', 'G-L2DZPV8S00')` network call still fires,
and click the footer's Hostinger/Mercato/Malt links to confirm the `lead=` and
`utm_*` query string on each click still matches what that page had before
migration (compare against the `git diff` from the regeneration step above).

## Prove nothing else moved (SC-004)

Screenshot the same four pages at a phone width and at desktop width, before and
after regeneration, and diff them visually. Only the listed unifications
(footer link set made consistent per locale, see spec.md FR-009) should show.

## Add a new page later

1. Add its header/footer region markers to the new HTML file.
2. Add `_shared/pages/<new-page>.json` with `file`, `header_family`,
   `header_locale`, `footer_locale`, and every `vars` key its templates need.
3. Run `python3 _shared/render.py`, commit the rendered file and the new JSON.
