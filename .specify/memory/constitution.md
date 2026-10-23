# nicogaraycons Constitution

## Core Principles

### I. Plain static output
What GitHub Pages serves is plain HTML, CSS and JS committed on `main`. Every page
must render its full content, navigation and footer without JavaScript, because
search engines, link previews and visitors with scripts blocked read the raw HTML.
No framework and no runtime dependency are added to the served pages.

### II. Tracking is part of the page (NON-NEGOTIABLE)
Every page loads GA4 (`G-L2DZPV8S00`) directly, and `assets/track.js` adds the
custom events described in `docs/analytics-conversions.md`. A change may not drop,
rename or break an existing tag, event, `data-cta` hook, `lead=` or `utm_*`
parameter unless the change is about that tracking. Before merge, existing and new
tracking is verified in a real browser on the real domain or a faithful local copy,
never only by reading the code.

### III. SEO signals stay intact
Canonical URLs, `hreflang` pairs, JSON-LD, `rel="sponsored nofollow"` on affiliate
links, the sitemap and the `/go/` redirect pages are preserved byte for byte in
meaning. Moved URLs keep a redirect page, since Pages cannot send server redirects.

### IV. Mobile first
Every visible change is checked at a phone width first, then desktop, with a
Playwright screenshot before it ships.

### V. Small, reviewable changes
Each change goes through a branch and a pull request. Generated or bulk edits must
produce a diff a human can review, and a single command must be able to reproduce
them.

## Content and language

Pages are in French or English according to their locale. Repository artifacts
(code, comments, commit messages, pull requests, specs, docs) are in English. Public
content never mentions Claude, Claude Code or AI attribution, and never exposes
secrets.

## Workflow

Branch, pull request, review by Nico, merge to `main`, then GitHub Pages publishes
within a few minutes. After merge, the live page is fetched to confirm the change is
online. Anything under the repository root is publicly served (`.nojekyll`), so
specs and docs must contain nothing private.

## Governance

This constitution overrides habits. Amendments are made through a pull request that
states the reason and bumps the version.

**Version**: 1.0.0 | **Ratified**: 2026-10-23 | **Last Amended**: 2026-10-23
