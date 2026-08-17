---
description: Copy selected decisions, questions, or TODOs from an investigation into global/, with a back-reference to the source — the investigation's original entry is never edited
argument-hint: [feature-slug, optional inside a workspace]
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, Skill, AskUserQuestion
---

Make part of an investigation's record **official**: copy it into `global/`
so every other investigation can rely on it. This is a copy, never a move —
the investigation's own entry stays exactly as it was.

First read the spec at `${CLAUDE_PLUGIN_ROOT}/docs/spec.md` and follow its
formats and resolution rules exactly, especially "Promotion".

Argument: `$ARGUMENTS`

## Steps

1. **Resolve** the workspace and active investigation per the spec.
2. **Ask what to promote, in prose** (free-form — this isn't a
   multiple-choice moment): specific IDs (`D-004`, `Q-002`, ...), a
   description of the content, or "everything reusable." If the answer is
   vague or "everything," propose candidates yourself rather than promoting
   blindly:
   - **accepted** decisions and **answered** questions are natural
     candidates — they're settled;
   - open questions, unresolved TODOs, and `proposed` decisions are unusual
     to promote — flag that explicitly and confirm before including any
     ("Q-003 is still open — promote it as an open global question, or wait
     until it's answered?").
3. **Dedup each candidate against `global/`** before writing:
   - for questions/TODOs, run the `bluewright:question-todo-triage` skill's
     dedup step against `global/questions.md`/`global/todo.md` — a match
     means "already global," report the existing ID instead of duplicating;
   - for decisions, compare the **Decision** text against
     `global/decisions.md`; an equivalent already there means nothing new
     to write — report the existing ID.
4. **Copy what's left into `global/<file>.md`:**
   - decisions → append via the `bluewright:decision-entry` skill, targeting
     `global/decisions.md`, with `Links:` including "promoted from
     `<slug>/decisions.md#D-00X`";
   - questions → append to `global/questions.md` with the next `Q-###`,
     `Raised:` noting "promoted from `<slug>/questions.md#Q-00X`";
   - TODOs → append to `global/todo.md` with the next `T-###`, text ending
     "(promoted from `<slug>/todo.md#T-00X`)".
   The investigation's original entry is **never** edited — this is
   purely additive.
5. **Ripple promoted decisions** through `bluewright:decision-entry`'s usual
   logic, scoped to `global/`: if a promoted decision answers an open
   `global/questions.md` entry, mark it answered.
6. **Report** a one-screen mapping: `<slug>/<file>.md#<old-ID>` →
   `global/<file>.md#<new-ID>` for everything promoted, plus what was
   skipped because an equivalent was already global, and what the user
   chose not to promote.

## Rules

- Copy only — never remove or edit an investigation's original entry.
- Never invent a promotion: only what the user selected (or explicitly
  confirmed from your proposed candidates) gets copied.
- `global/`'s ID sequences are independent of the investigation's; a
  promoted entry gets a new ID, not its old one.
- Touch nothing outside the workspace tree.
