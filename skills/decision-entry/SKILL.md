---
name: decision-entry
description: Record a decision in a Bluewright decisions.md — global or investigation-scoped — ADR-lite format, ID allocation, supersede flow, and the ripple updates to questions.md and todo.md. Use whenever a choice is made or reversed (approach picked, option ruled out, assumption accepted) at either scope.
---

# Recording a decision

The canonical file format lives in the plugin spec
(`${CLAUDE_PLUGIN_ROOT}/docs/spec.md`, section "decisions.md") — follow it
exactly. It is the same format whether the target is `global/decisions.md`
or an investigation's `decisions.md`; this skill covers the procedure and
the quality bar for either.

## What counts as a decision

Record an entry when something now constrains the design that didn't before:
an approach was picked, an option was ruled out, an assumption was accepted as
true, a stakeholder imposed a constraint. If the user merely *suggested* or
*asked* — that is a question or a TODO, not a decision. Never invent a
decision the user hasn't actually made; propose one with `Status: proposed`
instead when the evidence clearly points somewhere.

## Procedure

1. Read the target `decisions.md` (global or investigation — whichever the
   caller named); the next ID is the highest existing `D-###` in *that
   file* plus one (IDs are never reused, numbering never restarts, and
   global's sequence is independent of any investigation's).
2. Append the new entry at the BOTTOM of the file, per the spec format.
3. The log is append-only, with exactly one permitted edit of old entries:
   when a new decision supersedes `D-00X`, change that entry's `Status:` line
   to `superseded by D-0YY` — touch nothing else in it.
4. Ripple the decision through the other spine files, at the **same scope**
   as the target `decisions.md`:
   - `questions.md` — any question this decision answers gets
     `Status: answered` and an **Answer:** line referencing the D-ID;
   - `todo.md` — tick TODOs the decision completes; add new ones its
     Consequences imply (next `T-###`);
   - `investigation.yml` — update `status` to `closed` if this decision
     concludes the investigation (investigation scope only).
   If a decision recorded in an investigation turns out to be reusable
   beyond it, that's not this skill's job — point at
   `/bluewright:promote` instead of editing `KNOWLEDGE.md` or `global/`
   directly.
5. Report the entry ID and every ripple made.

## Quality bar

- **Context** states the forces: what was true, what conflicted, why now.
  A reader in six months must understand why this was hard.
- **Decision** is one paragraph, active voice, no hedging: "We use X."
- **Consequences** name what this commits us to AND what it rules out —
  a consequences section with no downside is a smell.
- **Links** connect the evidence: Q-IDs answered, `inputs/` files, external
  URLs, and — for a decision promoted from an investigation — its source
  entry. A decision without links is unverifiable.
- Title is short and imperative ("Use outbox pattern for ledger events"),
  not a sentence about the process ("Discussed ledger options").
