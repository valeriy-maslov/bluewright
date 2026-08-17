---
description: Interactively analyze captured information — global and the active investigation — without changing anything
argument-hint: [a question, or empty to be asked]
allowed-tools: Read, Glob, Grep, Bash
---

Answer questions about what's already been captured. Read-only, like
`/bluewright:status` — this command changes nothing, ever; it's for
understanding the record, not adding to it.

First read the spec at `${CLAUDE_PLUGIN_ROOT}/docs/spec.md` and follow its
resolution rules exactly.

Question: `$ARGUMENTS`

## Steps

1. **Resolve** the workspace per the spec. Resolve the active investigation
   if the cwd is inside one, or the argument names something that looks like
   a slug rather than a question; otherwise this is a global-only session —
   say so up front so the user knows the scope.
2. **Load the record**: `global/decisions.md`, `global/questions.md`,
   `global/todo.md`, and a targeted look at `global/inputs/` for anything
   relevant — plus, if an investigation is active, its own `decisions.md`,
   `questions.md`, `todo.md`, and `inputs/`. Treat global as the
   authoritative background and the investigation as the specifics on top of
   it; if they conflict, say so rather than picking one silently.
3. **Take the question** from `$ARGUMENTS`; if it's empty, ask what to
   explore.
4. **Answer grounded in the record.** Cite what you're drawing on every
   time — `D-###`, `Q-###`, `T-###`, or an `inputs/` file — and say "not
   captured yet" rather than inferring an answer the files don't support.
   Distinguish clearly between what's recorded and any reasoning you're
   layering on top of it.
5. **Stay conversational.** This is a dialogue: keep answering follow-ups in
   the same terms without re-resolving the workspace or re-explaining scope
   each time, unless the user changes topic to a different investigation.
6. **Surface, don't fix.** If a question exposes a gap, a conflict, or
   something worth tracking, say so plainly and point at
   `/bluewright:capture` (investigation-scoped) or `/bluewright:capture-global`
   — never write anything yourself, no matter how obvious the fix looks.

## Rules

- Strictly read-only — no writes, no ID allocation, no fixing drift you
  notice; just answer and, where relevant, flag it.
- Stay inside the workspace tree and whatever watchlist paths are already on
  record — this command doesn't fetch anything new (that's `/bluewright:sync`'s
  job) and doesn't reach the network.
- Every non-obvious claim traces to something in the record; "I think" is
  fine, "the record says" is better, and the two must never be blurred.
