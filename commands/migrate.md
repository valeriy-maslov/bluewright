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
formats and "Migrating from 1.x" section exactly.

Target: `$ARGUMENTS`

## Steps

1. **Resolve the workspace.** Use the argument as a path if given, otherwise
   walk up from cwd to the nearest `workspace.yml` per the spec. None found →
   stop and explain.
2. **Read versions.** Compare `workspace.yml`'s `bluewright` field (missing
   → treat as `1.0.0`) against the installed plugin version (from
   `${CLAUDE_PLUGIN_ROOT}/.claude-plugin/plugin.json`).
   - Equal → say the workspace is already current and stop; nothing to do.
   - Workspace newer than the plugin → stop: the installed plugin is older,
     update it first (same rule the hook enforces elsewhere).
3. **Survey what needs to change**, without writing anything yet:
   - is `global/` missing?
   - for each `<slug>/investigation.yml`: does it still have a `phase:`
     field instead of `status:`?
   - for each investigation: does `outputs/` exist where `artifacts/`
     doesn't?
   - are there `spikes/` folders? (these are left alone — see step 5 — but
     worth naming in the summary so the user isn't surprised later.)
   Present this survey and ask for confirmation before changing anything —
   a real yes/no moment, so `AskUserQuestion` is the right tool here.
4. **Migrate the workspace root:**
   - if `global/` is missing, scaffold it exactly as `/bluewright:init`
     does: `decisions.md`, `questions.md`, `todo.md` seeded with headers
     and no entries, `inputs/` and `artifacts/` with `.gitkeep`.
5. **Migrate each investigation:**
   - `investigation.yml` — replace a `phase: <value>` line with
     `status: <value>` per the spec's mapping table, touching nothing else
     in the file (field order, comments, other values all stay put).
   - if `outputs/` exists and `artifacts/` doesn't, `git mv outputs/
     artifacts/` (plain `mv` if the workspace isn't a git repo or the path
     isn't tracked). If both exist, stop and ask the user to reconcile
     manually rather than guessing which wins.
   - `spikes/<name>/` folders are **not** touched — they're no longer part
     of the managed layout, but their `SPIKE.md`/`VERDICT.md`/code are real
     history. Leave them exactly where they are.
6. **Bump the version.** Set `workspace.yml`'s `bluewright` field to the
   installed plugin version. This and `/bluewright:init` are the only
   commands allowed to write this field.
7. **Report** one screen: what was scaffolded, which investigations had
   their `phase`/`outputs/` migrated (with the phase→status mapping used
   for each), any `spikes/` folders left as unmanaged history, and the new
   `bluewright` version on record.

## Rules

- **Additive and renames only. Never delete data.** No decision, question,
  TODO, or input is ever touched — only `investigation.yml`'s phase field,
  folder names, and `workspace.yml`'s version field change.
- **Idempotent.** Re-running against an already-migrated workspace (or one
  migrated in a previous partial run) changes nothing further for the parts
  already done — check each condition (step 3) rather than assuming a
  clean-slate run.
- If a step's precondition doesn't hold (e.g. both `outputs/` and
  `artifacts/` exist), stop and ask rather than guessing.
- Touch nothing outside the workspace tree.
