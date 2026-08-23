---
description: Create a Bluewright workspace (workspace.yml + KNOWLEDGE.md + global/) at the given path
argument-hint: [path to workspace folder]
allowed-tools: Read, Write, Glob, Bash, AskUserQuestion
---

Create a new Bluewright **workspace** — the per-product/per-team container
that all investigations live in.

First read the spec at `${CLAUDE_PLUGIN_ROOT}/docs/spec.md` and follow its
formats exactly.

Target path: `$ARGUMENTS`

## Steps

1. **Resolve the target.** Use the argument as the workspace path (expand `~`,
   resolve relative to cwd). If no argument was given, propose the current
   working directory and confirm before using it — a bounded yes/no, so use
   `AskUserQuestion` (`Use this directory` / `Choose a different path`).
2. **Guard.**
   - If the target (or any of its ancestors) already contains a
     `workspace.yml`, stop: nested workspaces are not allowed. Report which
     workspace was found and where.
   - If the target exists and is non-empty, list what is there and confirm
     before proceeding (initializing inside an existing folder is fine —
     overwriting files is not; never overwrite an existing file) — another
     bounded yes/no, so use `AskUserQuestion` (`Proceed anyway` / `Cancel`).
3. **Interview, briefly — in plain text.** Ask in one conversational
   message for: workspace name (default: folder name), team/product name,
   anything to watch by default across every investigation — an issue
   tracker query, a wiki space, a repo, whatever the team actually uses.
   Turn each into a `defaults.watchlist` entry per the spec's watchlist
   entry shape (`type: repo` for a local clone, `type: external` with a
   free-text `label`/`query` for anything else — Bluewright has no
   built-in integration with any specific tool, so don't assume one).
   These are free-form answers — do NOT use AskUserQuestion for them (it
   requires 2–4 predefined options per question and rejects the call
   otherwise); just ask in prose. Reserve AskUserQuestion for genuine
   multiple-choice moments only. Every answer is optional — write an empty
   `watchlist: []` for anything skipped; entries can be added to
   `workspace.yml` later.
4. **Create** the folder (if needed), then `workspace.yml` and `KNOWLEDGE.md`
   per the spec, with today's date and the interview answers. Set the
   `bluewright` field to the installed plugin version — read it from
   `${CLAUDE_PLUGIN_ROOT}/.claude-plugin/plugin.json`; never hardcode it.
5. **Scaffold `global/`** — the workspace's official, workspace-wide record:
   `decisions.md`, `questions.md`, `todo.md` seeded with their headers and
   no entries, plus `inputs/` and `artifacts/` (each with a `.gitkeep`).
6. **Git.** If the target is not inside a git repository
   (`git rev-parse --git-dir` fails there), run `git init` in it. Do not
   commit — leave that to the user.
7. **Report.** Show the created layout, and point to the next steps: `cd`
   into the workspace, optionally run `/bluewright:capture-global` to record
   anything already known workspace-wide, then `/bluewright:new
   <feature-slug>` for the first investigation.

## Rules

- Touch nothing outside the target path.
- Never overwrite an existing file; if `workspace.yml` already exists at the
  target itself, report that this is already a workspace and stop.
