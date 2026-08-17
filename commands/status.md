---
description: One-screen overview of an investigation — status, next TODOs, open questions, latest decisions, sync freshness, plus a global-record glance
argument-hint: [feature-slug, optional inside a workspace]
allowed-tools: Read, Glob, Grep, Bash
---

Show a **one-screen status** of a Bluewright investigation. Read-only: this
command changes nothing, ever.

First read the spec at `${CLAUDE_PLUGIN_ROOT}/docs/spec.md` and follow its
resolution rules exactly.

Argument: `$ARGUMENTS`

## Steps

1. **Resolve** the workspace per the spec. Read a quick **Global** line
   first (see step 3) regardless of what follows. Then resolve the
   investigation: cwd inside one → that one; else the argument slug; else —
   if the workspace has exactly one investigation use it, and if it has
   several show the **workspace overview** instead (one line per
   investigation: title, status, open-question count, last sync) and stop.
2. **Read the spine**: `investigation.yml`, `decisions.md`, `questions.md`,
   `todo.md`, plus a glance at `artifacts/` and `global/questions.md` /
   `global/decisions.md`.
3. **Render one screen**, nothing more:

   - **Global** — one line: open question count in `global/questions.md`,
     and the latest `global/decisions.md` entry (title + ID).
   - **Header** — title, slug, status, created date.
   - **Next up** — the `Now` section of `todo.md`, top 5 max.
   - **Open questions** — blocking ones first (those with a `Blocks:` value),
     then the rest; count the total.
   - **Latest decisions** — the last 3 entry titles with IDs and dates.
   - **Sync** — `sync.last_run`, or "never".
   - **Flags** — only lines that are true:
     - last sync older than 7 days (or never) while a watchlist exists;
     - `artifacts/` older than the newest decision (stale shared artifacts);
     - `todo.md` `Now` section empty while `status` is not `closed`.

4. Close with the single most useful next command, chosen from the flags
   (e.g. `/bluewright:sync` if stale, `/bluewright:make-artifact` if
   artifacts lag).

## Rules

- Strictly read-only — no writes, no fixes, no ID allocation, even if you
  notice format drift; just flag it.
- Compact over complete: this is a glance, not a report. Never exceed one
  screen; link to files instead of quoting them.
