# nicogaraycons Constitution

## Core Principles

### I. Static First, Minimal Moving Parts
The site MUST stay plain static HTML, CSS and JavaScript served by GitHub Pages from `main`,
with no build step and no framework. Each page is a self-contained `index.html` in its own
directory; shared assets live in `assets/`. Any server-side logic a feature needs MUST live
outside this site (for example a serverless function on another host) behind a narrow,
documented HTTP contract, and the page MUST remain usable when that function is down.

### II. No Prices, Remote-First Positioning
No price, day rate or package cost MAY appear anywhere on nicogaray.com. Pages MUST keep the
"100 % remote" positioning and the AI agent integration offer aimed at small and mid-sized
companies (10 to 250 people). Every page ends with a clear path to book a discovery call.

### III. Brand Consistency
New pages MUST reuse the existing design tokens (`--bg`, `--accent`, `--text`, `--muted`,
`--radius`...) and the Google Sans typeface, and MUST look like the rest of the site. No visual
ships without being opened and captured with Playwright at desktop and phone widths, then
corrected from the capture.

### IV. Bilingual Content, English Repository
Visitor-facing copy exists in French (root) and English (`/en`). Everything else committed to
this repository, including code, comments, commit messages, specs, plans and docs, and any text
inside versioned images, MUST be in English. French copy MUST follow French typography (accents
on capitals, non-breaking space before `: ; ! ?`, « guillemets ») and MUST NOT use em or en dashes.

### V. Security and Abuse Resistance (NON-NEGOTIABLE)
No secret (API key, token) MAY ever be committed or shipped to the browser. Any endpoint that
calls a paid AI model MUST enforce origin checks, input length limits, rate limiting per client
and a global spending cap, and MUST treat visitor input as untrusted data, never as instructions
that change its system behavior. Visitor input MUST NOT be stored beyond what the feature states,
and the page MUST say so in plain words.

## Performance, SEO and Measurement

Pages MUST keep a Lighthouse performance score of 90 or more on mobile, ship accessible markup
(landmarks, labels, focus states, WCAG AA contrast) and include title, meta description,
canonical, hreflang between FR and EN, Open Graph and JSON-LD like the existing pages. New pages
are added to `sitemap.xml`. Conversions (form submits, booking clicks, demo runs) are tracked
through `assets/track.js` and documented in `docs/analytics-conversions.md`.

## Development Workflow and Quality Gates

Work happens on a feature branch, never on `main`. Substantial features follow Spec Kit:
specify, clarify when needed, plan, tasks, analyze, implement, converge. Nico validates the
spec (the what) and the plan (the how) before implementation starts. A pull request is merged
only after the Playwright captures are reviewed and, for anything that goes online with a new
endpoint or third-party script, after the `security-auditor` agent has reviewed it.

## Governance

This constitution supersedes other practices in this repository. Amendments are made through
`speckit-constitution`, recorded with a version bump (MAJOR for removed or redefined
principles, MINOR for new principles or sections, PATCH for wording) and reviewed in the pull
request that introduces them. Every spec and plan MUST include a constitution check.

**Version**: 1.0.0 | **Ratified**: 2026-09-29 | **Last Amended**: 2026-09-29
