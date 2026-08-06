---
description: One-screen overview of an investigation — phase, next TODOs, open questions, latest decisions, sync freshness
argument-hint: [feature-slug, optional inside a workspace]
allowed-tools: Read, Glob, Grep, Bash
---

Show a **one-screen status** of a Bluewright investigation. Read-only: this
command changes nothing, ever.

First read the spec at `${CLAUDE_PLUGIN_ROOT}/docs/spec.md` and follow its
resolution rules exactly.

Argument: `$ARGUMENTS`

## Steps

1. **Resolve** the workspace per the spec. Then resolve the investigation:
   cwd inside one → that one; else the argument slug; else — if the workspace
   has exactly one investigation use it, and if it has several show the
   **workspace overview** instead (one line per investigation: title, phase,
   open-question count, last sync) and stop.
2. **Read the spine**: `investigation.yml`, `decisions.md`, `questions.md`,
   `todo.md`, plus a glance at `spikes/*/VERDICT.md` and `outputs/`.
3. **Render one screen**, nothing more:

   - **Header** — title, slug, phase, created date.
   - **Next up** — the `Now` section of `todo.md`, top 5 max.
   - **Open questions** — blocking ones first (those with a `Blocks:` value),
     then the rest; count the total.
   - **Latest decisions** — the last 3 entry titles with IDs and dates.
   - **Sync** — `sync.last_run`, or "never".
   - **Flags** — only lines that are true:
     - a question blocks `design` while phase is `share` or `design`;
     - last sync older than 7 days (or never) while a watchlist exists;
     - `outputs/` older than the newest decision (stale shared artifacts);
     - `todo.md` `Now` section empty while phase is not `done`;
     - spike folders without a `VERDICT.md`.

4. Close with the single most useful next command, chosen from the flags
   (e.g. `/bluewright:sync` if stale, `/bluewright:publish` if outputs lag).

## Rules

- Strictly read-only — no writes, no fixes, no ID allocation, even if you
  notice format drift; just flag it.
- Compact over complete: this is a glance, not a report. Never exceed one
  screen; link to files instead of quoting them.
