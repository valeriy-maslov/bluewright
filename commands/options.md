---
description: Option analysis — agree candidates and criteria, research each in parallel, produce outputs/options.md with a scored comparison and a proposed decision
argument-hint: [feature-slug, optional inside a workspace]
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, Task, Skill, AskUserQuestion
---

Run the **option analysis** of a Bluewright investigation: enumerate the
credible approaches, research them side by side, and land a proposed
decision — the pivot from "what do we need" to "how will we do it".

First read the spec at `${CLAUDE_PLUGIN_ROOT}/docs/spec.md` and follow its
formats and resolution rules exactly.

Argument: `$ARGUMENTS`

## Steps

1. **Resolve** the workspace and investigation per the spec.
2. **Precondition.** Read `outputs/brief.md`. If it doesn't exist, say the
   analysis will be much weaker without it and ask whether to run
   `/bluewright:brief` first (recommended) or proceed from `inputs/` alone.
   Also read `questions.md`: list any open question that blocks option
   choice, and confirm the user wants to proceed despite them.
3. **Agree the frame with the user before any research.** Propose, then
   confirm in one round:
   - **candidates** — 2 to 5 credible approaches (from the brief, survey
     constraints, and your knowledge). The user can add, drop, or reword.
     Fewer than 2 means there is nothing to decide — say so and stop;
   - **criteria** — what will actually discriminate (must-have NFRs and
     constraints by ID, plus judgment criteria like operational burden,
     team fit, reversibility). Mark must-haves: violating one eliminates.
4. **Dispatch one `bluewright:option-scout` per candidate, in parallel**
   (single message), each with: its candidate description, the FR/NFR/C list
   from the brief, the agreed criteria, relevant survey excerpts, and the
   watchlist repo paths as `allowedPaths`.
5. **Synthesize `outputs/options.md`:**
   - the agreed criteria (must-haves marked);
   - the comparison matrix — candidates × criteria/requirements, from the
     scouts' uniform digests; violations of must-haves shown as eliminating;
   - per candidate: summary, risks, unknowns, effort, what it forecloses;
   - a **recommendation with reasoning** — which candidate and why, or
     explicitly "no winner until spike X settles unknown Y";
   - scouts' `spawnedIdeas` worth a look, if any.
6. **Ripple.**
   - Recommendation → a `Status: proposed` decision entry via the
     `bluewright:decision-entry` skill (the user accepts it later — do not
     mark it accepted yourself);
   - each unknown that needs a spike → `questions.md` + a `todo.md` entry
     ("spike: ..."), so `/bluewright:spike` can pick it up;
   - eliminated candidates get one line in the proposed entry's Context —
     ruling out is also a decision.
7. **Report** one screen: candidates researched, the matrix verdict in two
   sentences, the proposed D-ID, spike candidates, and the next step —
   usually `/bluewright:spike <name>` or accepting the proposed decision
   via `/bluewright:capture`.

## Rules

- Never start research before the user has confirmed candidates and
  criteria — scouting the wrong list wastes the whole fan-out.
- Scouts gather evidence; the comparison and recommendation happen here,
  in the open, traceable to digest fields — never "the agent said so".
- The proposed decision is `proposed`, never `accepted`, no matter how
  clear-cut the matrix looks.
- Re-running `/options` regenerates `outputs/options.md`, but prior decision
  entries and Q/T IDs stay untouched — extend, don't rewrite history.
