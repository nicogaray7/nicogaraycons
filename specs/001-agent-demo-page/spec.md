# Feature Specification: AI Agent Showcase Page with Live Demo

**Feature Branch**: `agent-demo-page`

**Created**: 2026-09-29

**Status**: Draft

**Input**: User description: "Create an MVP on nicogaray.com inspired by rerun.build: a showcase page for the AI agent offer plus a real AI demo, where a visitor describes a repetitive task and gets back a concrete agent plan (trigger, steps, tools, human approvals)."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Get an agent plan for my own task (Priority: P1)

A manager of a small or mid-sized company lands on the page, types a repetitive task their team
does (for example "we chase unpaid invoices by email every Monday"), and within seconds receives
a concrete plan for an AI agent that would handle it: what triggers it, the steps it runs, the
tools it connects to, where a human must approve, and the time it could save. From the result
they can book a discovery call in one click.

**Why this priority**: This is the feature that makes the page different from any other
consultant site. It proves know-how on the visitor's own problem and turns curiosity into a
qualified lead.

**Independent Test**: Open the page alone, submit three different task descriptions, check that
each returns a readable plan with all five parts and a working booking link.

**Acceptance Scenarios**:

1. **Given** a visitor on the page, **When** they submit a task description of 20 to 600
   characters, **Then** they see a progress state and then a plan with trigger, steps, tools,
   human approval points and an estimated time saved, in the page language.
2. **Given** a plan is displayed, **When** the visitor clicks the call to action, **Then** they
   reach the existing discovery call booking path.
3. **Given** a visitor who does not know what to type, **When** they click one of the example
   prompts, **Then** the field is filled with that example and they can submit it.
4. **Given** a task description that is not a business task (off topic, abusive, or trying to
   change the assistant's instructions), **When** it is submitted, **Then** the visitor gets a
   polite message inviting them to describe a business task, and no other content is produced.

---

### User Story 2 - Understand the offer at a glance (Priority: P2)

A visitor who does not try the demo scrolls the page and understands, without reading long
text, what an AI agent built by Nico does: a hero with an animated agent run (tasks moving from
running to completed), ready-made agent examples for small companies (invoice follow-up, lead
qualification, competitor watch, CRM reporting), an interactive human approval card showing that
nothing sensitive happens without consent, the tools that can be connected, a comparison with
manual work and generic tools, and a FAQ.

**Why this priority**: Most visitors will not type anything. The page must convert on its own
and it also works if the demo is unavailable.

**Independent Test**: Load the page with the demo service switched off; every section renders,
the animated run plays, the approval card responds to clicks, and the booking link works.

**Acceptance Scenarios**:

1. **Given** the page loads, **When** the hero is visible, **Then** an animated agent run shows
   at least three tasks changing state, and it respects the visitor's reduced motion setting.
2. **Given** the approval card, **When** the visitor clicks "Allow once", "Always" or "Refuse",
   **Then** the card shows the matching outcome without leaving the page.
3. **Given** any section of the page, **When** it is read, **Then** no price appears anywhere
   and the "100 % remote" positioning is stated.

---

### User Story 3 - Reach the page from the rest of the site and from search (Priority: P3)

The page is linked from the home page navigation and the services section, is listed in the
sitemap, has proper search and social metadata, and has an English version linked from `/en`.

**Why this priority**: Without entry points the page gets no traffic, but the page and the demo
deliver value first.

**Independent Test**: From the home page, reach the new page in one click; check the sitemap,
the page metadata and the language switch.

**Acceptance Scenarios**:

1. **Given** the French home page, **When** the visitor uses the navigation, **Then** the new
   page is one click away.
2. **Given** the French page, **When** the visitor switches language, **Then** they reach the
   English page with equivalent content, and vice versa.

---

### Edge Cases

- The demo service is down, slow (more than 20 seconds) or over its daily budget: the visitor
  sees a friendly message with example plans already shown on the page and the booking link;
  the rest of the page is unaffected.
- A visitor submits many requests in a row: after the per-visitor limit they are told to try
  again later and invited to book a call.
- Empty, too short (under 20 characters) or too long (over 600 characters) input: the form
  explains the limit before sending anything.
- The visitor pastes personal or confidential data: the page states beforehand that input is
  not stored and should not contain personal data.
- The visitor's browser has JavaScript disabled: the page content is readable and the booking
  link works; the demo shows a short note that it needs JavaScript.
- A request coming from another website tries to use the demo service: it is refused.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The page MUST let a visitor type a task description (20 to 600 characters) and
  submit it to get an AI-generated agent plan.
- **FR-002**: Each plan MUST contain: a short agent name, the trigger, 3 to 7 ordered steps, the
  tools involved, at least one human approval point when an action is sensitive (sending,
  paying, deleting, changing customer data), and an estimated time saved per week.
- **FR-003**: The plan MUST be written in the page language (French on the French page, English
  on the English page).
- **FR-004**: The page MUST offer at least four example prompts that fill the field on click.
- **FR-005**: The demo MUST refuse off-topic requests and attempts to override its instructions,
  and answer only with an invitation to describe a business task.
- **FR-006**: The demo MUST limit usage per visitor (default: 5 plans per hour) and globally
  (default: a daily budget cap), and show a clear message when a limit is reached.
- **FR-007**: The demo MUST accept requests only from nicogaray.com pages.
- **FR-008**: Visitor task descriptions MUST NOT be stored beyond what is needed to answer and to
  count usage, except when the visitor leaves their email (FR-008b), and the page MUST say so
  next to the field.
- **FR-008b**: After a plan is displayed, the visitor MAY leave their email, with an explicit
  unticked consent box, to receive the plan by email and be contacted by Nico. The email, the
  plan, the page language and the consent date are kept for 12 months at most, then deleted, and
  deleted earlier on request. Nico receives a copy of each lead.
- **FR-009**: Every plan MUST end with a call to action to book a discovery call, reusing the
  site's existing booking path.
- **FR-010**: The page MUST include: a hero with an animated agent run, agent examples for small
  companies, an interactive human approval card, a grid of connectable tools using the site's
  existing logos, a comparison (manual work vs generic tool vs custom agent), a FAQ and a final
  call to action.
- **FR-011**: The page MUST contain no price and MUST state the "100 % remote" positioning.
- **FR-012**: The page MUST remain fully readable and convert (booking link) when the demo is
  unavailable or JavaScript is disabled.
- **FR-013**: The page MUST track: demo submitted, plan displayed, demo error or limit reached,
  example prompt used, and booking click from the page.
- **FR-014**: The page MUST be linked from the home page and listed in the sitemap, with search
  and social metadata consistent with the other pages.
- **FR-015**: The page MUST exist in French and English with a language switch, both shipped
  in this MVP.

### Key Entities

- **Task description**: free text typed by the visitor, 20 to 600 characters, page language.
- **Agent plan**: name, trigger, ordered steps, tools, approval points, estimated time saved.
- **Lead**: email, consent timestamp, page language, the plan sent; retained 12 months at most.
- **Usage counter**: number of plans per visitor per hour and total per day, used only to
  enforce limits.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: A visitor gets a complete plan in under 15 seconds in 95 % of successful requests.
- **SC-002**: 9 out of 10 test prompts drawn from real small business tasks produce a plan Nico
  judges relevant and credible.
- **SC-003**: 100 % of a set of 10 off-topic or instruction-override prompts are refused.
- **SC-004**: The demo cost never exceeds the daily cap, verified by sending requests beyond it.
- **SC-005**: Within 30 days of launch, at least 20 % of page visitors try the demo and at least
  5 % of demo users click the booking call to action or leave their email.
- **SC-007**: A visitor who leaves their email receives the plan within 2 minutes.
- **SC-006**: The page scores 90 or more for mobile performance and accessibility, and has no
  horizontal scroll at phone width.

## Clarifications

### Session 2026-09-29

- Q: After the plan, booking link only or also email capture? → A: Email capture plus booking
  link (FR-008b).
- Q: English version in the MVP? → A: Yes, French and English ship together (FR-015).

## Assumptions

- The page lives at `/agents-ia/` in French and `/en/ai-agents/` in English; the name can change
  at planning.
- The discovery call booking path is the one already used by the home page contact section.
- The demo relies on a hosted AI model called through a small service outside GitHub Pages,
  since the site is static; its choice is a planning decision.
- Default limits: 5 plans per visitor per hour, and a daily cap on model spending that Nico sets
  at planning (proposed: a few euros per day).
- The demo produces a plan only; it does not run any agent or connect to any visitor tool.
- Tool logos come from the existing `assets/logos` set; no new brand assets are drawn.
- The security-auditor agent reviews the demo service and the page before it goes online.
