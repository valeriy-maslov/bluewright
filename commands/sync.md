---
description: Walk the watchlist for external changes since last sync and assess which decisions/assumptions they affect
argument-hint: [feature-slug, optional inside a workspace]
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, Task, ToolSearch, AskUserQuestion
---

Run a **watchlist sync**: find what changed in the outside world since the
last run, and answer the only question that matters — **which of this
investigation's assumptions moved**. Composable with /loop or a schedule:
must run to a useful end without user interaction.

First read the spec at `${CLAUDE_PLUGIN_ROOT}/docs/spec.md` and follow its
formats and resolution rules exactly.

Argument: `$ARGUMENTS`

## Steps

1. **Resolve** the workspace and investigation per the spec. Read the
   effective watchlist (workspace defaults + investigation entries) and
   `sync.last_run` from `investigation.yml` — if null, use the
   investigation's `created` date. An empty watchlist → say so and stop.
2. **Gather changes since `last_run`**, per entry type:
   - `repo` — in the entry's local clone: `git fetch --quiet` (best effort —
     on failure note it and use local state), then
     `git log <branch> --since=<last_run> --oneline --name-only` (prefer the
     remote-tracking ref when ahead). Collect hash, subject, changed files.
   - `external` — use `ToolSearch` to look for an MCP tool that plausibly
     serves this entry's `label`/`query` (e.g. an issue-search, page-fetch,
     or query tool from a connected server whose name or description echoes
     the label). If exactly one plausible match exists, run it with the
     entry's `query`, narrowed to changes since `last_run` in whatever way
     that tool supports; collect item id/title and what changed. If nothing
     matches, mark the entry `skipped: no tool found for "<label>"`. If more
     than one tool looks equally plausible, don't guess — mark it
     `skipped: ambiguous match for "<label>"` instead of querying the wrong
     system.
   Never fail the whole sync over one entry — record the error and move on.
3. **Short-circuit if quiet.** No changes anywhere → append a one-line
   "quiet" section to `sync-log.md`, update `sync.last_run` to now
   (ISO-8601), report, done.
4. **Assess.** Dispatch one `bluewright:impact-assessor` (Task) with the
   investigation path, the collected `changes[]`, and the watched repo
   paths. Do not pre-filter "obviously irrelevant" changes — relevance is
   the assessor's judgment, not the gatherer's.
5. **Ripple the hits** from the ImpactDigest:
   - `breaks` / `weakens` on a D-### → raise a question ("Does <change>
     overturn D-00X?", Blocks: that decision's area) and flag it prominently
     — never silently supersede a decision (same principle as /capture);
   - `answers` a Q-### → record the answer with the evidence reference;
   - `informs` → a `todo.md` entry or a watchlist `note` update, whichever
     fits;
   - a fact other investigations would care about → note it in your report
     and suggest `/bluewright:promote` or `/bluewright:capture-global` rather
     than writing to `global/` yourself.
6. **Record.** Append the run section to `sync-log.md` per the spec (per
   entry: change counts + skips; impact one-liners with IDs raised), then
   set `sync.last_run` to now. `/sync` is the only writer of both.
7. **Report** one screen: changes found per entry, hits with their class and
   the IDs created, skipped entries and why, and — if anything `breaks` —
   the explicit callout that a decision needs re-ruling.

## Rules

- The gatherer collects, the assessor judges, the ripples follow /capture's
  invariants: nothing lost, nothing silently decided.
- Watchlist paths and queries are the boundary: touch nothing else, and
  never write inside a watched repo (no pulls, no checkouts — fetch only).
- If `last_run` is in the future (clock skew, manual edit), say so and ask
  before proceeding — except in non-interactive runs, where you note it in
  `sync-log.md` and use the created date instead.
