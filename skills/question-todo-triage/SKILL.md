---
name: question-todo-triage
description: Turn raw captured material into candidate questions.md/todo.md entries through a guided conversation instead of auto-filing everything inferable — filters hard, dedups against the target file and (for investigation-scope capture) against global/, and writes only what the user confirms. Use from /bluewright:capture and /bluewright:capture-global whenever material might contain open questions or actionable items.
---

# Facilitating questions and TODOs

The failure mode this skill exists to prevent: an agent that infers every
possible ambiguity from a paragraph of notes and silently files ten
speculative `Q-###`/`T-###` entries, most of which are too deep, too
detailed, or already known — a swamp the user then has to wade through.
This skill's job is to think *with* the user about what's worth tracking,
not to decide for them.

## Inputs

- `targetPath` — the `questions.md` and `todo.md` to write into: either
  `global/` or one investigation's folder.
- `material` — the raw text just preserved to `inputs/` by the calling
  command (already saved verbatim before this skill runs — nothing is lost
  even if nothing here gets written).
- `crossCheckGlobal` — `true` when `targetPath` is an investigation (dedup
  also checks `global/questions.md` / `global/todo.md`); `false` when
  `targetPath` already is `global/`.

## Procedure

1. **Extract candidates, filtered hard.** A question only becomes a
   candidate if answering it would actually change a decision, a
   requirement, or the next concrete step — not every open-ended musing in
   the material. A TODO only becomes a candidate if it's a concrete,
   near-term action someone could start today. Merge near-duplicate
   phrasings of the same underlying unknown before candidates are even
   presented; never present five wordings of one question.
2. **Cap what you show at once.** Up to four candidates per round —
   `AskUserQuestion` (used in steps 3-4 below) caps at four questions per
   call, so one round maps to exactly one call. If the material implies
   more, name the theme ("there's a cluster of unknowns about the ledger
   API") and ask in prose which of them matter enough to track at all —
   that filtering judgment is open-ended, not a fixed set of options, so it
   stays conversational even though the rest of this procedure doesn't.
3. **Dedup before presenting each candidate.**
   - Always check `targetPath`'s own `questions.md`/`todo.md` for an
     existing equivalent.
   - When `crossCheckGlobal` is true, also check `global/questions.md` and
     `global/todo.md` — global is the authoritative tier, so a near-match
     there matters more than one in another investigation.
   - On a match, don't create a new ID yet — this is a bounded choice, so
     ask via `AskUserQuestion` with options `Reuse Q-00X` (or `T-00X`) and
     `Drop it`. Don't add a third predefined option for "reword it as a new
     entry" — the tool's automatic "Other" field already covers that: if
     the user types a phrasing there instead of picking an option, treat
     that text as the confirmed wording for a genuinely new, separate
     entry, not as a rejection of the question.
4. **Present the remaining (non-matched) candidates via `AskUserQuestion`**,
   batched per the four-per-round cap above. For each candidate, put the
   phrasing and one line on why it seemed to matter into the question text,
   with `Accept as written` and `Drop it` as the fixed options — again rely
   on the automatic "Other" field for "accept, but with this wording
   instead." (A candidate with a dedup match was already resolved in step 3
   and doesn't need to be re-presented here.)
5. **Write only what's confirmed.** Allocate the next ID in the target file
   at write time, per the spec's sequential/never-reused rule — never
   pre-allocate IDs for candidates that might be dropped.
6. **Say plainly what happened to the rest.** Anything not surfaced, or
   surfaced and dropped, is not lost — it's already sitting verbatim in
   `inputs/` from the calling command's preserve-first step. Say so, so the
   user knows "not tracked" isn't "discarded."

## Rules

- Never write a `Q-###`/`T-###` the user didn't actually confirm.
- Never skip the dedup pass to save a round-trip — a duplicate is worse
  than one extra question to the user.
- This skill only ever writes `questions.md`/`todo.md`. Decisions go
  through the `bluewright:decision-entry` skill instead.
