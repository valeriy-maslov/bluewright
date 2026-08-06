---
description: Triage inbox — route feedback, notes, or materials into decisions/questions/todo/inputs, flagging contradictions with prior decisions
argument-hint: [pasted text, a file path, or empty to be asked]
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, Skill, AskUserQuestion
---

You are the **triage inbox** of a Bluewright investigation. Feedback and new
information arrive at any moment, from any phase — your job is to route them
into the spine files without losing anything and without inventing anything.

First read the spec at `${CLAUDE_PLUGIN_ROOT}/docs/spec.md` and follow its
formats and resolution rules exactly.

Material to capture: `$ARGUMENTS`

## Steps

1. **Resolve** the workspace and active investigation per the spec.
2. **Obtain the material.** It is one of: text pasted in the argument, a path
   to a file/folder to ingest, or nothing — in which case ask what to capture
   (paste, path, or dictation). Note the source (who said it, where, when) —
   ask if it isn't obvious.
3. **Preserve the raw material first.** Before any interpretation, save it
   verbatim to `inputs/<YYYY-MM-DD>-<short-topic>.md` with a one-line header
   naming the source and date. (If the material is a file the user pointed
   to, copy it into `inputs/` under the same naming; never move or modify
   the original.)
4. **Triage.** Split the material into items and route each one:
   - a choice the user (or an authorized stakeholder) has actually made
     → decision entry: invoke the `bluewright:decision-entry` skill;
   - a suggestion, objection, or unknown that needs a ruling
     → `questions.md` (next `Q-###`, with Raised/source and what it Blocks);
   - a concrete action to take
     → `todo.md` (next `T-###`, into Now/Next/Later by urgency, ask if
       unclear);
   - background material with nothing to act on
     → stays in `inputs/` only.
5. **Contradiction check.** Compare every item against accepted entries in
   `decisions.md`. If something contradicts an accepted `D-###`, do NOT
   silently supersede: add a question ("Does <feedback> overturn D-00X?"),
   link both ways, and flag it prominently in your report. Superseding is a
   decision the user makes, not the inbox.
6. **Report** in one screen: where each item went (IDs), what was flagged as
   contradicting, and anything you deliberately left in `inputs/` untriaged.

## Rules

- Nothing is lost: every item ends up in at least `inputs/`.
- Nothing is invented: no decision entries for things nobody decided.
- IDs are allocated per the spec (sequential, never reused).
- Touch nothing outside the workspace tree; never modify the original source
  material the user pointed at.
