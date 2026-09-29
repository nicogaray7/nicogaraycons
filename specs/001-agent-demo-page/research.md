# Research: AI Agent Showcase Page with Live Demo

## R1. Where the demo logic runs

- **Decision**: A Cloudflare Worker, `agent-demo-api`, on the existing Cloudflare account.
- **Rationale**: GitHub Pages is static. The bot already has full Cloudflare access, so deploy
  and bindings need no new vendor. Bindings keep keys out of code. Free tier covers the traffic.
- **Alternatives considered**: An endpoint on the VPS (adds exposure and uptime risk on the
  machine that runs the bot); Supabase Edge Functions (new vendor, no gain); Vercel functions
  (the site just left Vercel).

## R2. Which model

- **Decision**: Workers AI `@cf/meta/llama-3.3-70b-instruct-fp8-fast` with JSON schema output,
  temperature 0.3, max 900 output tokens. `@cf/openai/gpt-oss-120b` is the fallback candidate if
  French quality fails SC-002 in testing.
- **Rationale**: Good French and structured output, no external key, about 160 neurons per plan,
  so roughly 60 plans a day inside the 10,000 free neurons, then $0.011 per 1,000 neurons on
  Workers Paid (under 0.2 cent per plan).
- **Alternatives considered**: Claude through the Anthropic API (best quality, needs a paid API
  key stored as a Worker secret and a separate budget; kept as an upgrade path); smaller models
  such as Mistral 7B (cheaper but weaker plans in French).

## R3. Abuse and cost control

- **Decision**: Four layers: origin allow-list; Turnstile invisible token checked server side;
  Workers Rate Limiting binding, 5 plans per IP per hour; D1 `daily_usage` counter with a hard
  cap (default 150 plans a day, a `DAILY_CAP` variable). Input 20 to 600 characters.
- **Rationale**: Origin alone is spoofable by scripts; Turnstile blocks them without friction;
  the daily cap bounds the worst case whatever happens.
- **Alternatives considered**: CAPTCHA with a challenge (hurts conversion); KV counters
  (eventually consistent, can overshoot the cap).

## R4. Prompt injection and off-topic input

- **Decision**: Visitor text goes only in the user message, wrapped as data; the system prompt
  states the single job and forbids prices, links and code; the output must match a strict JSON
  schema with a `status` field (`ok` or `refused`); the Worker validates the JSON and renders
  text only (no HTML) on the page.
- **Rationale**: A schema-bound output cannot carry arbitrary content to the page, and refusals
  are machine-checkable for SC-003.

## R5. Sending the plan by email

- **Decision**: Cloudflare Email Service send binding from `agents@nicogaray.com`, after the
  sending domain is onboarded (SPF and DKIM records). One mail to the visitor with the plan, one
  copy to garaynico.ng@gmail.com with the lead.
- **Rationale**: Same platform, binding instead of API key, any recipient once the domain is
  onboarded. New accounts get a conservative daily quota, well above expected leads.
- **Alternatives considered**: Resend (needs an API key secret and its own DNS records); Hostinger
  SMTP relayed from the VPS (Workers cannot open SMTP easily and it couples the site to the VPS).
- **Open point for Nico**: the DNS records must be added where nicogaray.com is managed. If the
  domain is not on Cloudflare DNS, the records are added at the current DNS host.

## R6. Personal data (GDPR)

- **Decision**: Consent box unticked by default with a one-line purpose; store email, plan JSON,
  locale, consent timestamp; a daily scheduled Worker run deletes leads older than 12 months;
  deletion on request by email; the privacy note next to the form says all this.
- **Rationale**: Minimal data for the stated purpose, explicit consent, bounded retention.

## R7. Page design and assets

- **Decision**: Reuse the site tokens (`--bg #07080f`, `--accent #5b6ef5`, `--green #34d399`,
  `--radius 14px`) and Google Sans; reuse `assets/logos` for the tool grid; the hero animation
  and approval card are CSS plus a few lines of JS, paused under `prefers-reduced-motion`.
  Design work goes through `ui-ux-pro-max` and `kit-ui-web`, with Playwright captures.
- **Rationale**: Visual continuity with the site and no new dependency.

## R8. Page URLs

- **Decision**: `/agents-ia/` (French) and `/en/ai-agents/` (English), cross-linked with
  hreflang, added to the navigation of `index.html` and `en/index.html` and to `sitemap.xml`.
