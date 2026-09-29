# Contract: agent-demo-api

Base URL: the Worker route (for example `https://agent-demo-api.<account>.workers.dev`, or
`https://api.nicogaray.com` if the zone is on Cloudflare). All requests must carry
`Origin: https://nicogaray.com`; any other origin gets `403` with no CORS headers.

## POST /plan

Request (JSON): `{ "task": string, "locale": "fr" | "en", "turnstileToken": string }`

| Status | Body | Meaning |
|--------|------|---------|
| 200 | `AgentPlan` with `status: "ok"` | Plan generated |
| 200 | `AgentPlan` with `status: "refused"` and `message` | Off-topic or override attempt |
| 400 | `{ "error": "invalid_input" }` | Length or locale out of range |
| 403 | `{ "error": "forbidden" }` | Bad origin or failed Turnstile |
| 429 | `{ "error": "rate_limited", "retryAfter": seconds }` | Per-IP limit |
| 503 | `{ "error": "daily_cap" }` | Daily cap reached |
| 502 | `{ "error": "model_error" }` | Model failed or returned invalid JSON twice |

Timeout: the page aborts after 20 s and shows the fallback.

## POST /lead

Request (JSON): `{ "email": string, "consent": true, "locale": "fr" | "en", "plan": AgentPlan,
"turnstileToken": string }`

The Worker re-validates the plan against the schema before storing it.

| Status | Body | Meaning |
|--------|------|---------|
| 201 | `{ "ok": true }` | Lead stored, emails queued |
| 400 | `{ "error": "invalid_input" }` | Bad email, missing consent, invalid plan |
| 403 / 429 | as above | Origin, Turnstile or rate limit |

## Scheduled

Daily cron: delete `leads` older than 12 months; delete `daily_usage` rows older than 30 days.

## Front-end tracking events (`assets/track.js`)

`agent_demo_submit`, `agent_demo_plan_shown`, `agent_demo_refused`, `agent_demo_error`
(with `reason`), `agent_demo_example_click`, `agent_demo_lead_submit`, `agent_page_booking_click`.
