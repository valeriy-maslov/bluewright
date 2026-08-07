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
formats and resolution rules exactly. Then load three skills:
`bluewright:solution-design` (template and quality bar),
`bluewright:plantuml-conventions` (diagrams), and `bluewright:item-triage`
(levels and deduplication — `/design` both consumes and produces items).

Argument: `$ARGUMENTS`

## Steps

1. **Resolve** the workspace and investigation per the spec.
2. **Gate.** Check readiness and tell the user exactly where they stand:
   - an **accepted** decision on the approach exists in `decisions.md`
     (a `proposed` one is not enough — point at it and ask for the ruling
     via `/bluewright:capture` first);
   - no active question in `questions.md` has `Blocks: design`;
   - spikes without verdicts are named as loose ends.
   The user may override each gap explicitly; every overridden gap must
   appear in the design's "Risks and open items" — a gap waved through is
   still a gap.
3. **Promote the parked design work.** Set `phase: design` and run the
   altitude gate: every `Level: design` entry in `questions.md` `## Parked`
   moves to `## Active` (`Status: open`), and every `level: design` entry in
   `todo.md` `## Parked` moves to `Next`. This is the moment the deferred
   detail was deferred *to* — these are the questions the design must
   actually settle. Deduplicate as you promote, per the item-triage skill:
   a pile parked over weeks usually contains several entries on one decision,
   and rolling them up here is proposed to the user before it is applied.
   `Level: build` entries stay parked — they are ticket material (step 8).
   Report the promoted count before writing anything.
4. **Gather the record**: `outputs/brief.md` (requirement IDs), `outputs/
   options.md` (winner and runners-up), all accepted decisions, every spike
   `VERDICT.md`, the newly promoted design-level questions, the workspace
   `KNOWLEDGE.md` (cross-team facts, watchlist owners for section 7).
5. **Write `outputs/design.md`** per the solution-design skill — every
   section, every claim traceable to a D-###, verdict, requirement ID, or
   source. Answer the promoted design-level questions here: each one is
   either settled by the design (mark it answered, referencing the section
   that settles it) or genuinely still open (carry it into section 8). Where
   the record is silent, do NOT fill the silence: raise a `Q-###`, list it in
   section 8, and move on.
6. **Diagrams** per the plantuml-conventions skill: context always; deeper
   levels only where the design changes something. `.puml` files into
   `outputs/`, referenced from section 4 as `.png` links (rendering itself
   happens in `/bluewright:publish`).
7. **Ripple.**
   - `investigation.yml` → `phase: design` (already set in step 3);
   - propose (never self-accept) a decision entry "Adopt solution design v1"
     via `bluewright:decision-entry`, linking the design;
   - tick completed TODOs; surviving open items become TODOs for
     implementation follow-up, at `level: build` and therefore parked —
     they are the next team's list, not this investigation's;
   - update the investigation's line in `KNOWLEDGE.md`.
8. **Tickets (offer, don't assume).** If the user wants the breakdown now:
   derive tickets from design sections 5 and 7, **and from the `build`-level
   parked entries in `questions.md` and `todo.md`** — that pile is exactly
   the implementation detail the investigation collected and set aside, and
   this is where it is finally worth something. Each ticket references its
   subsection, requirement IDs, and the Q/T IDs it discharges; discharged
   entries move to `## Closed` / `Done` referencing the ticket. Write the
   result to `outputs/tickets.md` (shareable draft); create actual Jira
   issues only if the user explicitly asks and Jira MCP tools are available.
9. **Report** one screen: where the design is, what it rests on (counts:
   decisions, verdicts, requirements covered/unmet), how many parked
   questions the promotion pulled in and how many the design settled, open
   items carried into section 8, and the next step — `/bluewright:publish`
   to render and ship it.

## Rules

- Synthesis only: an unmade choice discovered mid-writing becomes a
  question, never a silent authorial decision — the design reflects the
  log, it never front-runs it.
- Requirement IDs, D-IDs, Q-IDs are quoted verbatim from their files —
  never renumbered, never paraphrased into untraceability.
- Re-running `/design` regenerates `outputs/design.md` from the current
  record; it never edits history in the spine files.
