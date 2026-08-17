---
name: solution-design
description: The template and quality bar for a Bluewright solution design document — an artifact/design.md-shaped write-up presented to a team and broken down into implementation tickets. Use from /bluewright:make-artifact when the ask is a solution design, or when writing/reviewing one directly.
---

# Writing a solution design

A solution design serves two readers at once: the **team** deciding whether
to buy in (they need the why), and the **implementer** deriving tickets
(they need the what, precisely). Every section below exists for one of
those two — don't drop sections, mark them `n/a — <reason>` if truly empty.

## Template — artifacts/design.md

```markdown
# <Title — the feature, not the process>
- Status: draft | in review | agreed
- Date: YYYY-MM-DD · Investigation: <slug, or "workspace-wide" for a global artifact>
- Decisions this rests on: D-00X, D-00Y, ...

## 1. Context and goal
Why this exists, in one page max. Goal and explicit non-goals.

## 2. Requirements
What the feature must do and the constraints it must respect, drawn from
`inputs/` and accepted decisions — cite the source (`inputs/<file>`,
`D-00X`) for each. There is no fixed ID scheme for these; state them
plainly and traceably instead of inventing one.

## 3. Chosen approach
The approach in one paragraph, then WHY — distilled from the accepted
decisions. Name any alternatives that were seriously considered and the
one sentence each that ruled them out (readers always ask "did you
consider X?").

## 4. Architecture
The diagrams (see plantuml-conventions): context first, then container/
component as depth requires. Each diagram: one paragraph of prose — what to
look at, what changed vs today.

## 5. Detailed design
Components and responsibilities, data model changes, API/event contracts,
failure modes and their handling. Precise enough that a ticket can point at
a subsection.

## 6. Non-functional handling
Performance, scale, security, operability — how each is met, measured, or
explicitly deferred.

## 7. Rollout and migration
Order of operations, feature flags, data migration, backout plan,
cross-team dependencies (from the watchlist — who must know).

## 8. Risks and open items
Accepted risks with mitigations; open Q-### that survive into
implementation, each with its blast radius.

## 9. References
Key decisions, `inputs/` sources, external references.
```

## Rules

- **Traceability is the whole point**: every claim traces to a D-###, an
  `inputs/` source, or a cited external reference. A design that can't show
  its receipts reopens every debate in the review meeting.
- The design **synthesizes, it never decides**: if writing it surfaces an
  unmade choice, that's a question or decision to raise via
  `/bluewright:capture` first — the design reflects the log, never
  front-runs it.
- Self-contained: readable by someone who has seen nothing else; all links
  relative within `artifacts/` or absolute URLs.
- Ticket-ready: sections 5 and 7 are structured so implementation tickets
  can be cut per subsection.
