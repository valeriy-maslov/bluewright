---
description: Bring a workspace's on-disk format up to date with the installed plugin version — additive and renames only, never deletes data
argument-hint: [path to workspace, optional — defaults to the resolved workspace]
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, AskUserQuestion
---

Migrate a Bluewright **workspace** to the on-disk format the installed
plugin expects. This is the command the version hook points at when it
blocks a workspace as out of date — unlike every other `/bluewright:*`
command, it is allowed to run against a workspace whose format predates the
installed plugin.

First read the spec at `${CLAUDE_PLUGIN_ROOT}/docs/spec.md` and follow its
formats and "Migrating to 3.x" section exactly.

Target: `$ARGUMENTS`

## Steps

1. **Resolve the workspace.** Use the argument as a path if given, otherwise
   walk up from cwd to the nearest `workspace.yml` per the spec. None found →
   stop and explain.
2. **Require a clean git tree.** Run `git status --porcelain` at the
   workspace root; anything but empty output means stop and say so —
   uncommitted changes would mix with this command's edits and make `git
   diff` useless as a review. If the workspace isn't a git repository at
   all, note that there is no safety net and confirm before proceeding.
3. **Read versions.** Compare `workspace.yml`'s `bluewright` field (missing
   → treat as `1.0.0`) against the installed plugin version (from
   `${CLAUDE_PLUGIN_ROOT}/.claude-plugin/plugin.json`).
   - Equal → say the workspace is already current and stop; nothing to do.
   - Workspace newer than the plugin → stop: the installed plugin is older,
     update it first (same rule the hook enforces elsewhere).
   - Note whether the source is `2.0.0` specifically — it needs the extra
     `questions.md`/`todo.md` flattening in step 6; a plain `1.x` source
     doesn't.
   - Note whether the source predates `4.0.0` — it needs the
     `jira`/`confluence` → generic `external`/`links` conversion in steps 5
     and 6; a source already at `4.0.0`+ doesn't.
4. **Survey what needs to change**, without writing anything yet:
   - is `global/` missing?
   - for each `<slug>/investigation.yml`: does it still have a `phase:`
     field instead of `status:`?
   - for each investigation: does `outputs/` exist where `artifacts/`
     doesn't?
   - if the source is `2.0.0`: which `questions.md`/`todo.md` files still
     have `## Active`/`## Parked`/`## Closed` section headers or `Level:`
     fields?
   - if the source predates `4.0.0`: does `workspace.yml` still have
     `defaults.jira_project_keys`/`defaults.confluence_space`? Does any
     `investigation.yml` still have `links.jira_epic`/`links.confluence`,
     or watchlist entries with `type: jira`/`type: confluence`?
   - are there `spikes/` folders? (these are left alone — see step 5 — but
     worth naming in the summary so the user isn't surprised later.)
   Present this survey and ask for confirmation before changing anything —
   a real yes/no moment, so `AskUserQuestion` is the right tool here.
5. **Migrate the workspace root:**
   - if `global/` is missing, scaffold it exactly as `/bluewright:init`
     does: `decisions.md`, `questions.md`, `todo.md` seeded with headers
     and no entries, `inputs/` and `artifacts/` with `.gitkeep`.
   - if the source predates `4.0.0` and `workspace.yml` still has
     `defaults.jira_project_keys`/`defaults.confluence_space`, convert them
     per the spec's "Migrating to 4.x" table: each project key becomes an
     `external` entry appended to `defaults.watchlist`, the Confluence space
     (if set) becomes one more, then remove the two old fields. Skip fields
     that are already empty — nothing to convert.
6. **Migrate each investigation:**
   - `investigation.yml` — replace a `phase: <value>` line with
     `status: <value>` per the spec's mapping table, touching nothing else
     in the file (field order, comments, other values all stay put).
   - if `outputs/` exists and `artifacts/` doesn't, `git mv outputs/
     artifacts/` (plain `mv` if the workspace isn't a git repo or the path
     isn't tracked). If both exist, stop and ask the user to reconcile
     manually rather than guessing which wins.
   - if the source is `2.0.0` and `questions.md`/`todo.md` still show the
     altitude structure: flatten per the spec's `2.0.0` → `3.x` table —
     drop the `## Active`/`## Parked`/`## Closed` headers (entries flatten
     into one list, in that order), re-head entries from `### Q-00X` to
     `## Q-00X`, remap `Status: parked` → `open` and `Status: merged` →
     `dropped`, fold `## Parked` in `todo.md` into `## Later`. Leave
     `Level:` fields and `(level: …)` suffixes and any `**Evidence:**`/
     `Merged into:` lines exactly where they are — they're unparsed by
     `3.x` but deleting them would violate "never delete data" for no
     functional gain.
   - `spikes/<name>/` folders are **not** touched — they're no longer part
     of the managed layout, but their `SPIKE.md`/`VERDICT.md`/code are real
     history. Leave them exactly where they are.
   - if the source predates `4.0.0`, convert per the spec's "Migrating to
     4.x" table: `links.jira_epic` and each entry of `links.confluence`
     become free-text strings appended to `links: []`; each watchlist entry
     with `type: jira`/`type: confluence` becomes `type: external` with a
     `label`/`query` derived from its `jql`/`page_id`. Skip fields that are
     already empty or absent.
7. **Bump the version.** Set `workspace.yml`'s `bluewright` field to the
   installed plugin version. This and `/bluewright:init` are the only
   commands allowed to write this field.
8. **Report** one screen: what was scaffolded, which investigations had
   their `phase`/`outputs/` migrated (with the phase→status mapping used
   for each), whether `questions.md`/`todo.md` needed flattening and what
   changed, which `jira`/`confluence` fields or watchlist entries were
   converted to generic `external`/`links` entries and to what, any
   `spikes/` folders left as unmanaged history, and the new `bluewright`
   version on record. Close by reminding the user this command never
   commits — review with `git diff`, commit when satisfied.

## Rules

- **Additive and renames only. Never delete data.** No decision, question,
  or TODO entry, and no input, is ever deleted — only `investigation.yml`'s
  phase field, folder names, `questions.md`/`todo.md` section structure
  (2.0.0 sources only), `jira`/`confluence` fields and watchlist entry types
  (pre-4.0.0 sources only — converted, not dropped, to `external`/`links`),
  and `workspace.yml`'s version field change.
- **Requires a clean git tree and never commits.** `git diff` is the
  review, `git revert`/`git reset` is the undo — never run this against a
  dirty tree, and never commit on the user's behalf.
- **Idempotent.** Re-running against an already-migrated workspace (or one
  migrated in a previous partial run) changes nothing further for the parts
  already done — check each condition (step 4) rather than assuming a
  clean-slate run.
- If a step's precondition doesn't hold (e.g. both `outputs/` and
  `artifacts/` exist), stop and ask rather than guessing.
- Touch nothing outside the workspace tree.
