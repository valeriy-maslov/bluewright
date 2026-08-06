---
description: Synthesize the solution design (outputs/design.md + diagrams) from decisions, options, and spike verdicts; optionally draft implementation tickets
argument-hint: [feature-slug, optional inside a workspace]
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, Skill, AskUserQuestion
---

Write the **solution design** — the investigation's final product, the
document you present to the team and cut implementation tickets from. This
command synthesizes what the investigation has already established; it does
not make new choices.

First read the spec at `${CLAUDE_PLUGIN_ROOT}/docs/spec.md` and follow its
formats and resolution rules exactly. Then load both skills:
`bluewright:solution-design` (template and quality bar) and
`bluewright:plantuml-conventions` (diagrams).

Argument: `$ARGUMENTS`

## Steps

1. **Resolve** the workspace and investigation per the spec.
2. **Gate.** Check readiness and tell the user exactly where they stand:
   - an **accepted** decision on the approach exists in `decisions.md`
     (a `proposed` one is not enough — point at it and ask for the ruling
     via `/bluewright:capture` first);
   - no open question in `questions.md` has `Blocks: design`;
   - spikes without verdicts are named as loose ends.
   The user may override each gap explicitly; every overridden gap must
   appear in the design's "Risks and open items" — a gap waved through is
   still a gap.
3. **Gather the record**: `outputs/brief.md` (requirement IDs), `outputs/
   options.md` (winner and runners-up), all accepted decisions, every spike
   `VERDICT.md`, the workspace `KNOWLEDGE.md` (cross-team facts, watchlist
   owners for section 7).
4. **Write `outputs/design.md`** per the solution-design skill — every
   section, every claim traceable to a D-###, verdict, requirement ID, or
   source. Where the record is silent, do NOT fill the silence: raise a
   `Q-###`, list it in section 8, and move on.
5. **Diagrams** per the plantuml-conventions skill: context always; deeper
   levels only where the design changes something. `.puml` files into
   `outputs/`, referenced from section 4 as `.png` links (rendering itself
   happens in `/bluewright:publish`).
6. **Ripple.**
   - `investigation.yml` → `phase: design`;
   - propose (never self-accept) a decision entry "Adopt solution design v1"
     via `bluewright:decision-entry`, linking the design;
   - tick completed TODOs; the surviving open items become TODOs for
     implementation follow-up;
   - update the investigation's line in `KNOWLEDGE.md`.
7. **Tickets (offer, don't assume).** If the user wants the breakdown now:
   derive tickets from design sections 5 and 7 — each ticket references its
   subsection and requirement IDs. Write the result to `outputs/tickets.md`
   (shareable draft); create actual Jira issues only if the user explicitly
   asks and Jira MCP tools are available.
8. **Report** one screen: where the design is, what it rests on (counts:
   decisions, verdicts, requirements covered/unmet), open items carried
   into section 8, and the next step — `/bluewright:publish` to render and
   ship it.

## Rules

- Synthesis only: an unmade choice discovered mid-writing becomes a
  question, never a silent authorial decision — the design reflects the
  log, it never front-runs it.
- Requirement IDs, D-IDs, Q-IDs are quoted verbatim from their files —
  never renumbered, never paraphrased into untraceability.
- Re-running `/design` regenerates `outputs/design.md` from the current
  record; it never edits history in the spine files.
