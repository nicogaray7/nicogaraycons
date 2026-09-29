# Implementation Plan: AI Agent Showcase Page with Live Demo

**Branch**: `agent-demo-page` | **Date**: 2026-09-29 | **Spec**: [spec.md](spec.md)

**Input**: Feature specification from `/specs/001-agent-demo-page/spec.md`

## Summary

Two static pages on GitHub Pages (`/agents-ia/` in French, `/en/ai-agents/` in English) present
the AI agent offer in the style of rerun.build: animated agent run, agent templates for small
companies, interactive approval card, tool grid, comparison, FAQ. A small Cloudflare Worker
(`agent-demo-api`) turns a visitor's task description into a structured agent plan with Workers
AI, enforces origin, bot, rate and budget limits, and, when the visitor consents, stores the lead
in D1 and emails the plan to the visitor and a copy to Nico. The pages work without the Worker.

## Technical Context

**Language/Version**: HTML5, CSS, vanilla JavaScript (ES2020) for the pages; TypeScript on the
Cloudflare Workers runtime for the API.

**Primary Dependencies**: Workers AI (`@cf/meta/llama-3.3-70b-instruct-fp8-fast`, JSON schema
mode), Cloudflare Turnstile (invisible), Workers Rate Limiting binding, D1, Cloudflare Email
Service send binding. No front-end library. Wrangler for deploy.

**Storage**: D1 database `agent-demo` with two tables: `leads` and `daily_usage`. No task text is
stored unless it is part of a consented lead.

**Testing**: Vitest with `@cloudflare/vitest-pool-workers` for the Worker (contract, limits,
refusal); Playwright for the pages (desktop 1440 and phone 390 captures, demo happy path against
a mocked API, no-JS and API-down paths); Lighthouse CI on both pages.

**Target Platform**: Evergreen desktop and mobile browsers; Cloudflare edge for the API.

**Project Type**: Static web pages plus one serverless API.

**Performance Goals**: Plan displayed in under 15 s at p95 (SC-001); pages LCP under 2.5 s on
mobile, no layout shift from the demo block.

**Constraints**: No secret in the repository or the browser; origin allow-list
`https://nicogaray.com`; 20 to 600 characters input; 5 plans per IP per hour; daily plan cap
(default 150 plans, which stays in the Workers AI free allocation of 10,000 neurons most days,
about 160 neurons per plan); no price on the pages.

**Scale/Scope**: Tens to low hundreds of demo runs per day; 2 pages, 1 Worker, 1 D1 database.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Status | How the plan complies |
|-----------|--------|-----------------------|
| I. Static first | Pass | Pages stay plain static files; server logic lives in a separate Worker under `worker/`, not served as a page; pages degrade cleanly when it is down. |
| II. No prices, remote | Pass | Copy review task checks for any price and for the "100 % remote" statement; the model prompt forbids quoting prices. |
| III. Brand consistency | Pass | Reuse the `:root` tokens and Google Sans from `index.html`; Playwright captures at 1440 and 390 before merge. |
| IV. Bilingual, English repo | Pass | FR and EN pages; code, specs and commits in English; French copy checked for typography and dashes. |
| V. Security (non-negotiable) | Pass | Bindings only, no key in code; origin check, Turnstile, per-IP and daily caps, input limits, strict JSON schema output, prompt-injection refusal; consented leads only, 12-month purge; security-auditor review before go-live. |
| Performance, SEO, measurement | Pass | Lighthouse CI gate at 90; metadata, hreflang, JSON-LD, sitemap; events added to `assets/track.js` and documented. |
| Workflow | Pass | Feature branch, Nico validates spec and plan, PR with captures, security review. |

Post-design re-check: still passing, no violations to justify.

## Project Structure

### Documentation (this feature)

```text
specs/001-agent-demo-page/
├── plan.md
├── research.md
├── data-model.md
├── quickstart.md
├── contracts/
│   └── demo-api.md
└── tasks.md             # next stage
```

### Source Code (repository root)

```text
agents-ia/
└── index.html           # French page
en/ai-agents/
└── index.html           # English page
assets/
├── agents/
│   ├── agents.css       # page styles on top of the site tokens
│   ├── agents.js        # hero animation, approval card, demo form, lead form
│   └── examples.json    # static example plans (fallback when the API is down)
└── track.js             # + new demo events
worker/
├── wrangler.toml        # bindings: AI, DB, RATE_LIMITER, EMAIL, TURNSTILE secret name only
├── src/
│   ├── index.ts         # routing, CORS, origin check
│   ├── plan.ts          # prompt, JSON schema, model call, validation
│   ├── limits.ts        # rate limit + daily cap
│   ├── leads.ts         # consent, D1 insert, emails, purge job
│   └── prompts/         # system prompt FR and EN
├── migrations/
│   └── 0001_init.sql
└── test/
tests/e2e/
└── agents-page.spec.ts  # Playwright
index.html, en/index.html, sitemap.xml, docs/analytics-conversions.md  # links, sitemap, events
```

**Structure Decision**: Pages follow the existing one-directory-per-page convention. The Worker
lives in `worker/` in the same repository so the contract and the page change together; it has
no secrets in files, and GitHub Pages serving its source is harmless because the repository is
already public. `worker/` and `tests/` get an `index.html`-free layout so nothing there becomes a
page.

## Complexity Tracking

No constitution violations.
