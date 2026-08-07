---
name: decision-entry
description: Record a decision in a Bluewright investigation's decisions.md — ADR-lite format, ID allocation, supersede flow, and the ripple updates to questions.md, todo.md, and KNOWLEDGE.md. Use whenever a choice is made or reversed during an investigation (approach picked, option ruled out, assumption accepted, spike verdict adopted).
---

# Recording a decision

The canonical file format lives in the plugin spec
(`docs/spec.md` at the bluewright plugin root, section "decisions.md") —
follow it exactly. This skill covers the procedure and the quality bar.

## What counts as a decision

Record an entry when something now constrains the design that didn't before:
an approach was picked, an option was ruled out, an assumption was accepted as
true, a spike verdict was adopted, a stakeholder imposed a constraint. If the
user merely *suggested* or *asked* — that is a question or a TODO, not a
decision. Never invent a decision the user hasn't actually made; propose one
with `Status: proposed` instead when the evidence clearly points somewhere.

## Procedure

1. Read the investigation's `decisions.md`; the next ID is the highest
   existing `D-###` plus one (IDs are never reused, numbering never restarts).
2. Append the new entry at the BOTTOM of the file, per the spec format.
3. The log is append-only, with exactly one permitted edit of old entries:
   when a new decision supersedes `D-00X`, change that entry's `Status:` line
   to `superseded by D-0YY` — touch nothing else in it.
4. Ripple the decision through the other spine files. Load the
   `bluewright:item-triage` skill before writing to `questions.md` or
   `todo.md` — a decision's consequences are the classic source of
   fine-grained follow-ups that swamp a list:
   - `questions.md` — any question this decision answers gets
     `Status: answered`, an **Answer:** line referencing the D-ID, and moves
     to `## Closed`. Check `## Parked` too: settling an approach frequently
     answers questions that were parked precisely because the approach was
     unsettled;
   - `todo.md` — tick TODOs the decision completes; add new ones its
     Consequences imply (next `T-###`), each with its `(level: …)` and placed
     by the altitude gate. A decision made during `options` usually implies
     `design`-level work, which parks;
   - `KNOWLEDGE.md` (workspace root) — if the decision is reusable knowledge
     for other investigations (a system fact, an org constraint), update the
     investigation's index line or the Systems section;
   - `investigation.yml` — update `phase` if this decision moves it.
5. Report the entry ID and every ripple made — questions closed by name,
   new TODOs enumerated if active and counted by level if parked.

## Quality bar

- **Context** states the forces: what was true, what conflicted, why now.
  A reader in six months must understand why this was hard.
- **Decision** is one paragraph, active voice, no hedging: "We use X."
- **Consequences** name what this commits us to AND what it rules out —
  a consequences section with no downside is a smell.
- **Links** connect the evidence: Q-IDs answered, spike `VERDICT.md`,
  `inputs/` files, external URLs. A decision without links is unverifiable.
- Title is short and imperative ("Use outbox pattern for ledger events"),
  not a sentence about the process ("Discussed ledger options").
