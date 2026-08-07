---
name: item-triage
description: How a Bluewright investigation admits a question or a TODO — assign its altitude level (frame/options/design/build), deduplicate it against what already exists, roll several items up into one, and report the result by counts rather than by list. Use whenever a command is about to write to questions.md or todo.md (capture, brief, options, spike, sync, design, new, groom, migrate) or when an existing list has grown unmanageable.
---

# Admitting a question or a TODO

The canonical file formats live in the plugin spec (`docs/spec.md` at the
bluewright plugin root, sections "Altitude", "questions.md", "todo.md") —
follow them exactly. This skill covers the judgment: **what level an item is,
whether it is new at all, and when several items are really one.**

The failure this exists to prevent: a list that grows by a dozen items per
capture until it is a decision backlog nobody can face. Every item in it may be
individually reasonable — the harm is cumulative, so the discipline has to be
applied on every single write, not audited later.

## 1. Assign the level

Ask one question about the item: **what is the earliest phase at which
answering it changes anything?** That phase is the level.

| Level     | Assign when the answer…                                              | Example |
|-----------|----------------------------------------------------------------------|---------|
| `frame`   | changes the goal, a non-goal, a requirement (FR/NFR/C), or a constraint | "Are refunds in scope, or only payments?" |
| `options` | changes which approach wins, or eliminates a candidate                | "Can the ledger API be called synchronously at all?" |
| `design`  | assumes the approach is already fixed, and shapes `outputs/design.md` | "Where does the retry live — caller or gateway?" |
| `build`   | belongs in an implementation ticket, not in this investigation        | "What backoff multiplier do we use?" |

Tie-breaks, in order:

- **When torn between two levels, choose the lower one.** A `frame` item is
  put in front of the user immediately; the cost of wrongly promoting is an
  interruption, the cost of wrongly parking is a delay. Parking is reversible
  and `/bluewright:design` reverses it automatically.
- **Specificity is a strong signal.** An item naming a concrete mechanism,
  parameter, library, field name, or number is almost always `design` or
  `build`. An item naming a stakeholder, a scope boundary, or a business rule
  is almost always `frame`.
- **"It depends on a choice we haven't made" means the level is at least the
  level of that choice.** Anything downstream of an unpicked approach is
  `design` at the highest.
- A `Blocks:` value overrides the gate — an item that genuinely blocks
  something stays active whatever its level. Do not reach for `Blocks:` to
  keep an item visible; use it only when the named thing truly cannot proceed.

Then place the item per the spec's altitude gate: at or above the
investigation's current phase altitude → `## Active` / `Now`|`Next`|`Later`;
below it → `## Parked`.

## 2. Deduplicate before allocating an ID

**Never mint an ID before searching.** Grep the whole of `questions.md` and
`todo.md` — `Active` *and* `Parked`, not just what is currently visible — for
the item's subject, using more than one wording.

If an existing item is about the same underlying decision, do not create a new
one. Append a dated line to that item's `**Evidence:**` block instead:

```markdown
**Evidence:**
- 2026-08-07 (/capture, standup, Ann): timeouts seen in staging
```

(Create the `**Evidence:**` block if the entry doesn't have one yet.) New
material may also *raise* an item's altitude or add a `Blocks:` value — an
existing `design`-level question that turns out to eliminate an option becomes
`options`-level and moves to `Active`. Say so in the report.

Two items are the same when **one answer settles both**. They are different
when they could be answered in opposite directions independently — a shared
topic is not enough. "Which queue do we use?" and "Does the queue guarantee
ordering?" share a topic and are two questions.

## 3. Roll several items up into one

When three or more items serve a single underlying decision, they are one
question with sub-points, and the list is better for saying so.

Propose an umbrella item that absorbs them:

- the umbrella is the decision itself, phrased so it can be answered;
- each absorbed item's substance survives as an evidence line or a sub-point
  on the umbrella — a rollup that loses content is a deletion;
- each absorbed entry moves to `## Closed` with `Status: merged` and
  `Merged into: Q-###`. It keeps its ID and its text.

Nothing is deleted, nothing is renumbered, no ID is reused. A reader who
follows an old `Q-021` reference must still land on something that tells them
where it went.

**Rollup is proposed, never silently applied.** A command writing a handful of
items names the candidate rollup in its report and lets the user take it.
Bulk consolidation of an existing list is `/bluewright:groom`, which proposes
merges in batches and applies only what the user confirms.

## 4. Report by counts, not by list

The report is part of the problem or part of the fix. Rules:

- **enumerate** what landed in `Active` / `Now` — that is what the user must
  actually deal with;
- **count** what was parked, grouped by level:
  `Parked: 11 (design 8, build 3)`. Never list parked items; they are on
  disk and `/bluewright:status` summarises them;
- **name** every existing item that gained evidence — "added evidence to
  Q-007" — so the user sees that consolidation happened rather than assuming
  material was dropped;
- **flag** proposed rollups explicitly, with the umbrella and the IDs it
  would absorb.

A report that lists forty new IDs has already failed, whatever the files say.

## Quality bar

- A question is phrased so it *can* be answered — a topic ("error handling")
  is not a question; "Do we retry a failed ledger call, or fail the payment?"
  is.
- One item, one decision. If answering it requires making two independent
  choices, it is two items — or, more often, one item at a higher level.
- Levels are assigned from the item's content, never from where it came from.
  Feedback from a senior stakeholder about a variable name is still `build`.
- Nothing is lost: an item that doesn't earn a Q or a T still exists verbatim
  in `inputs/`. Parking and merging are bookkeeping, not deletion.
