---
description: Consolidate an investigation's questions and todos — re-level against the current phase, park what's below it, and merge duplicates with your confirmation
argument-hint: [feature-slug, optional inside a workspace]
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, Skill, AskUserQuestion
---

**Groom** an investigation's `questions.md` and `todo.md`: bring every item to
the right altitude and collapse the ones that are really the same item. Run it
whenever the active list has stopped being something you can act on — after a
run of captures, after a phase change, or when `/bluewright:status` says so.

Grooming never decides anything and never discards anything. It only changes
where an item sits and whether three entries are admitted to be one.

First read the spec at `${CLAUDE_PLUGIN_ROOT}/docs/spec.md` and follow its
formats and resolution rules exactly, then load the `bluewright:item-triage`
skill — it holds the level test, the sameness test, and the merge bookkeeping
this command applies in bulk.

Argument: `$ARGUMENTS`

## Steps

1. **Resolve** the workspace and investigation per the spec. Read
   `investigation.yml` for the current `phase` — that is the altitude
   everything is measured against.
2. **Inventory.** Read `questions.md` and `todo.md` in full, both active and
   parked sections. Report the starting counts by section and level before
   changing anything, so the user can see the size of the problem.
3. **Re-level and place — automatic, no confirmation.** For every open or
   parked item, apply the item-triage level test to its *content* and place it
   by the spec's altitude gate. Items move in both directions: a parked
   `design`-level question is promoted when the phase has reached `design`,
   and an active question that is really about implementation detail is parked
   whatever section it was written into. Items with a `Blocks:` value stay
   active regardless — but drop a `Blocks:` value that names something already
   decided or already delivered, and say which ones you dropped.
   Closed entries (`answered`, `dropped`, `merged`) are never touched.
4. **Cluster and propose merges — confirmation required.** Group the remaining
   items by the underlying decision each serves. Where three or more serve
   one decision, propose an umbrella. Present the proposals via
   AskUserQuestion **in batches of about five**, one question per cluster, so
   a long list stays reviewable:
   - show the proposed umbrella wording and the IDs it would absorb;
   - offer `merge` / `keep separate` / `park all` (park all: keep them
     distinct but drop them a level).
   Never propose a merge across levels that would raise an item's altitude
   without saying so, and never merge an entry that has a `Blocks:` value into
   one that doesn't.
5. **Apply** only what was confirmed. Absorbed entries move to `## Closed`
   with `Status: merged` and `Merged into: Q-###`, keeping their ID and their
   text; their substance is carried onto the umbrella as evidence lines or
   sub-points. Nothing is deleted, nothing is renumbered, no ID is reused.
6. **Report** the before/after counts by section and level, the merges
   applied, the `Blocks:` values dropped, and — if the active list is still
   long — say so honestly rather than declaring victory. A groom that halves
   a list nobody could face may still leave a list nobody can face.

## Rules

- **Bookkeeping only.** Grooming never answers a question, never ticks a TODO,
  never writes a decision, and never edits an item's substance beyond
  attaching it to an umbrella. If an item looks wrong, that is the user's call
  via `/bluewright:capture`, not this command's.
- **Nothing is lost.** Every ID that existed before still resolves after, and
  a reader following an old `Q-###` reference lands on an entry that says
  where it went.
- Levels come from the item's content, never from who raised it or how
  strongly it was worded.
- Idempotent: running `/bluewright:groom` twice with no captures in between
  changes nothing the second time. If it does, the level test was applied
  inconsistently — say so rather than churning the files.
- Touch nothing outside the investigation folder; never commit.
