---
description: Requirements analysis — digest inputs/, survey watched systems in parallel, produce outputs/brief.md, seed questions from the gaps
argument-hint: [feature-slug, optional inside a workspace]
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, Task, AskUserQuestion
---

Run the **requirements analysis** of a Bluewright investigation: turn
whatever is in `inputs/` plus the reality of the watched systems into
`outputs/brief.md` — the foundation `/options` and `/design` build on.

First read the spec at `${CLAUDE_PLUGIN_ROOT}/docs/spec.md` and follow its
formats and resolution rules exactly.

Argument: `$ARGUMENTS`

## Steps

1. **Resolve** the workspace and investigation per the spec.
2. **Precondition.** If `inputs/` holds nothing beyond `00-intake.md`, ask
   whether to proceed on the intake alone or stop to gather materials first.
   If `links.jira_epic` or `links.confluence` are set in `investigation.yml`
   and matching MCP tools are available in this session, offer to fetch those
   sources into `inputs/` (date-prefixed files, source noted) before analysis.
3. **Dispatch in parallel** (single message, one Task per agent):
   - one `bluewright:requirements-analyst` with the investigation path and
     the goal from `inputs/00-intake.md`;
   - one `bluewright:system-surveyor` per `type: repo` watchlist entry
     (effective watchlist = workspace defaults + investigation entries),
     each with its target path, branch, note, and topic keywords drawn from
     the goal. Skip paths that don't exist locally — report them as
     unavailable rather than failing.
4. **Synthesize `outputs/brief.md`** from the digests:
   - goal (one paragraph) and explicit non-goals;
   - requirements tables — FR/NFR/C with their IDs and sources (these IDs
     are permanent: options scoring and the design reference them);
   - domain glossary;
   - current-state summary per surveyed system: capabilities, integration
     surface, constraints the design must respect;
   - open points — every conflict, ambiguity, and gap, referencing the
     Q-IDs created in step 5.
   The brief must be self-contained and shareable: a colleague who has seen
   nothing else must be able to read it cold.
5. **Ripple.**
   - Every conflict/ambiguity/gap from the analyst → `questions.md`
     (next `Q-###`, `Raised: (source: /brief)`, with what it Blocks).
   - `changeSignals` from surveyors worth watching → `todo.md` or a note in
     the watchlist entry's `note` field.
   - Tick the bootstrap TODOs this completes; add follow-ups.
   - Set `phase: frame` → leave as is; `/brief` completing is the exit
     criterion the user confirms, not an automatic transition.
6. **Report** one screen: where the brief is, requirement counts, the
   surveyed systems and their relevance, new Q-IDs (blocking ones first),
   and the suggested next step — usually answering blockers via
   `/bluewright:capture`, then `/bluewright:options`.

## Rules

- Requirements are extracted, never invented; anything `inferred` by the
  analyst becomes a question to confirm, not a fact in the brief.
- Surveyors get only watchlist paths — never point them anywhere the user
  didn't explicitly list.
- Re-running `/brief` regenerates `outputs/brief.md` (it is derived, not a
  log) but must never renumber existing FR/NFR/C IDs still referenced
  elsewhere — extend, don't reshuffle.
