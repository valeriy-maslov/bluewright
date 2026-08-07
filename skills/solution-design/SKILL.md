---
name: solution-design
description: The template and quality bar for a Bluewright solution design document (outputs/design.md) — the final artifact of an investigation, written to be presented to a team and to be broken down into implementation tickets. Use when writing or reviewing a solution design.
---

# Writing a solution design

The design is the investigation's final product. It serves two readers at
once: the **team** deciding whether to buy in (they need the why), and the
**implementer** deriving tickets (they need the what, precisely). Every
section below exists for one of those two — don't drop sections, mark them
`n/a — <reason>` if truly empty.

## Template — outputs/design.md

```markdown
# <Title — the feature, not the process>
- Status: draft | in review | agreed
- Date: YYYY-MM-DD · Investigation: <slug>
- Decisions this rests on: D-00X, D-00Y, ...

## 1. Context and goal
Why this exists, in one page max. Goal and explicit non-goals.

## 2. Requirements
The FR/NFR/C tables FROM THE BRIEF, by ID — do not renumber, do not restate
differently. Mark any requirement the design consciously does not meet.

## 3. Chosen approach
The winning option in one paragraph, then WHY — distilled from options.md
and the accepted decisions. Name the runners-up and the one sentence each
that killed them (readers always ask "did you consider X?").

## 4. Architecture
The diagrams (see plantuml-conventions): context first, then container/
component as depth requires. Each diagram: one paragraph of prose — what to
look at, what changed vs today.

## 5. Detailed design
Components and responsibilities, data model changes, API/event contracts,
failure modes and their handling. Precise enough that a ticket can point at
a subsection.

## 6. Non-functional handling
Walk the NFR IDs: how each is met, measured, or explicitly deferred.

## 7. Rollout and migration
Order of operations, feature flags, data migration, backout plan,
cross-team dependencies (from the watchlist — who must know).

## 8. Risks and open items
Accepted risks with mitigations; active Q-### that survive into
implementation, each with its blast radius. Questions still parked at
`build` level are not listed here one by one — they are ticket material;
note their count and point at `outputs/tickets.md`.

## 9. References
Brief, options matrix, spike verdicts, key decisions, external sources.
```

## Rules

- **Traceability is the whole point**: every claim traces to a D-###, a
  spike verdict, a requirement ID, or a cited source. A design that can't
  show its receipts reopens every debate in the review meeting.
- The design **synthesizes, it never decides**: if writing it surfaces an
  unmade choice, that's a new question/decision entry first — the design
  reflects the log, never front-runs it.
- Self-contained: readable by someone who has seen nothing else; all links
  relative within `outputs/` or absolute URLs.
- Ticket-ready: sections 5 and 7 are structured so implementation tickets
  can be cut per subsection, each with its acceptance criteria implied by
  the requirement IDs it references.
