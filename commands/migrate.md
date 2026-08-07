---
description: Bring a workspace up to the installed plugin's format — convert every investigation's files, groom the backlog, and record the new version in workspace.yml
argument-hint: (no arguments — migrates the whole workspace)
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, Skill, AskUserQuestion
---

**Migrate** the current workspace to the installed plugin's format. This is the
command the version hook points at when it blocks: it converts every
investigation on disk, then records the new version in `workspace.yml`.

The version hook deliberately exempts this command, so it runs in exactly the
workspaces where everything else is blocked.

First read the spec at `${CLAUDE_PLUGIN_ROOT}/docs/spec.md` — it defines both
the target formats and the versioning rules — and load the
`bluewright:item-triage` skill, which holds the level test and merge
bookkeeping the conversion applies.

## Steps

1. **Resolve the workspace** per the spec (walk up from cwd to the nearest
   `workspace.yml`). This command works on the *whole workspace*, every
   investigation in it — not on one investigation, and it takes no argument.
2. **Read both versions.** The workspace's `bluewright:` field, and the target
   from `${CLAUDE_PLUGIN_ROOT}/.claude-plugin/plugin.json` — read it, never
   hardcode it. Then:
   - equal → report "already at v<X.Y.Z>, nothing to do" and stop;
   - workspace newer than the plugin → stop and say the plugin must be
     updated first (`/plugin update bluewright@bluewright`); migrating
     downward is not something this command does;
   - field missing → treat the workspace as the oldest released format and
     say so before proceeding;
   - workspace older → migrate.
3. **Require a clean tree.** Run `git status --porcelain` in the workspace. If
   it is dirty, stop and ask the user to commit or stash first — migration
   rewrites many files at once, and a clean starting point is what makes
   `git diff` a real review and `git revert` a real undo. The user may
   override explicitly; if they do, say plainly that the diff will be mixed.
   If the workspace is not a git repository at all, warn once and ask before
   continuing.
4. **Convert each investigation**, in turn, reporting as you go. For a
   workspace at format v1 (flat questions and todos, no levels):
   - `questions.md` — each flat `## Q-###` block becomes `### Q-###` under a
     section. `Status: answered` and `Status: dropped` entries move verbatim
     to `## Closed`. Each `Status: open` entry gets a `Level:` from the
     item-triage level test and lands in `## Active` or `## Parked` per the
     altitude gate, measured against that investigation's current `phase`.
     Any existing `Raised:` and `Blocks:` lines are preserved as written; an
     entry with a `Blocks:` value stays active.
   - `todo.md` — `Now` / `Next` / `Later` items get a `(level: …)` suffix,
     replacing any older `(phase: …)` suffix; those below the current altitude
     move to the new `## Parked` section. `Done` is untouched.
   - Then run the **groom pass** — the re-level, cluster, and merge procedure
     that `commands/groom.md` defines: re-levelling is automatic, and every
     merge is proposed in batches of about five and applied only if
     confirmed. On a list of a
     couple of hundred items this is the long part; say how many batches are
     coming before starting, and let the user decline merging entirely and
     take the conversion alone.
5. **Record the version.** Only after every investigation has converted, set
   `bluewright: "<target>"` in `workspace.yml`. Per the spec, `init` and
   `migrate` are the only writers of this field. If any investigation failed
   to convert, do NOT write it — a half-migrated workspace that claims the new
   version is worse than one that still asks to be migrated.
6. **Report**, per investigation: items in, and how they came out — active,
   parked (by level), closed, merged. Then the workspace line: old version →
   new version. Close with the review instructions: `git diff` to read it,
   `git revert` to undo it, `/bluewright:groom <slug>` to correct any
   levelling you disagree with.

## Rules

- **Never commit.** `/bluewright:init` doesn't, and neither does this — the
  diff is the user's to read and their commit to make.
- **Nothing is lost, nothing is renumbered.** Every `Q-###` and `T-###` that
  existed before the migration still resolves afterwards, in exactly one
  section, with its original text. Verify this before reporting success:
  compare the ID set before and after and say the count explicitly.
- **Levelling is judgment, and it will not be perfect** on a list of two
  hundred items. Say so in the report rather than implying otherwise, and
  point at `/bluewright:groom` as the correction.
- **Idempotent.** Re-running on an already-migrated workspace stops at step 2.
  A second run must never park a second time or re-open closed entries.
- Touch nothing outside the workspace tree — not watched repos, not the
  original sources of anything in `inputs/`.
