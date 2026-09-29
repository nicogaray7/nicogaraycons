# Data Model: AI Agent Showcase Page with Live Demo

## TaskRequest (not stored)

| Field | Type | Rules |
|-------|------|-------|
| task | string | Trimmed, 20 to 600 characters |
| locale | enum | `fr` or `en` |
| turnstileToken | string | Required, verified server side |

## AgentPlan (returned; stored only inside a Lead)

| Field | Type | Rules |
|-------|------|-------|
| status | enum | `ok` or `refused` |
| name | string | 2 to 60 characters, required when `ok` |
| trigger | string | Up to 160 characters |
| steps | array of string | 3 to 7 items, each up to 200 characters |
| tools | array of string | 1 to 8 items, each up to 40 characters |
| approvals | array of string | At least 1 when a step sends, pays, deletes or changes customer data |
| timeSavedHoursPerWeek | number | 0.5 to 40 |
| message | string | Required when `refused`: invitation to describe a business task |

## Lead (D1 table `leads`)

| Column | Type | Rules |
|--------|------|-------|
| id | TEXT | UUID, primary key |
| email | TEXT | Valid address, lowercased, up to 254 characters |
| locale | TEXT | `fr` or `en` |
| plan_json | TEXT | Validated AgentPlan with `status = ok` |
| consent_at | TEXT | ISO 8601 UTC, required |
| created_at | TEXT | ISO 8601 UTC |
| emailed_at | TEXT | Set when the visitor mail is accepted by the email service |

Lifecycle: created on consented submit → `emailed_at` set after sending → deleted by the daily
purge 12 months after `created_at`, or earlier on request.

## DailyUsage (D1 table `daily_usage`)

| Column | Type | Rules |
|--------|------|-------|
| day | TEXT | `YYYY-MM-DD` UTC, primary key |
| plans | INTEGER | Incremented before each model call; request refused when it reaches `DAILY_CAP` |

Per-IP limits live in the Rate Limiting binding and are not persisted.
