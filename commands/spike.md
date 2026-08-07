---
description: Scaffold, run, or conclude a time-boxed spike/PoC — ends in a VERDICT.md and a decision entry either way
argument-hint: [spike-name]
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, Skill, AskUserQuestion, WebFetch, WebSearch
---

Run a **spike**: a time-boxed experiment that settles one unknown with
evidence. A spike is not a prototype of the feature — it answers a question,
and it always ends in a verdict, even "inconclusive".

First read the spec at `${CLAUDE_PLUGIN_ROOT}/docs/spec.md` and follow its
formats and resolution rules exactly, and load the `bluewright:item-triage`
skill before writing anything to `questions.md` or `todo.md`.

Spike name: `$ARGUMENTS`

## Mode

Resolve the workspace and investigation per the spec, then look at
`spikes/<name>/`:

- doesn't exist → **scaffold** (step 1);
- exists without `VERDICT.md` → **work** (step 2), or **conclude** (step 3)
  if the user says the spike is done;
- has a `VERDICT.md` → it is closed; report the verdict and stop (a new
  question means a new spike, never reopening a concluded one).

## 1 — Scaffold

- Kebab-case name; if missing, derive one from the question and confirm.
- Establish the frame, in one round: **which unknown** this settles (pick
  from `questions.md` — `## Active` first, but a parked question is a
  legitimate spike target and gets promoted to active with its level raised
  when one is aimed at it — or from `unknowns` in `outputs/options.md`, or
  create the Q-### now at `Level: options`), **success criteria** (what
  result would
  prove/disprove it), and the **time-box**. Use AskUserQuestion only for
  picking the unknown, and only when two or more candidates exist (it
  requires 2–4 options per question); success criteria and time-box are
  free-form — ask for them in plain prose.
- Create `spikes/<name>/SPIKE.md` per the spec; tick/add the matching
  `todo.md` entry.
- A spike without a linked question is refused: if nobody can say what
  question it answers, it is not a spike.

## 2 — Work

- Everything lives inside `spikes/<name>/` — code, scripts, docker files,
  notes, measurements. Installing dependencies, running code, and hitting
  the network are allowed HERE (this is the sandbox the rest of the plugin
  doesn't have), but nothing outside the spike folder may be modified.
- Keep the success criteria in front: work that doesn't move toward them is
  scope creep — flag it instead of following it.
- Record observations as you go in the spike folder (e.g. `notes.md`), so
  the verdict can cite evidence, not memory.
- When the time-box is reached, say so and push toward concluding —
  "inconclusive, needs another time-box" is a legitimate verdict; silent
  overrun is not.

## 3 — Conclude

- Write `VERDICT.md` per the spec: result (proven/disproven/inconclusive),
  what was tried, evidence (files/measurements inside the spike folder),
  recommendation.
- Ripple via the `bluewright:decision-entry` skill: answer the linked
  Q-### referencing the verdict; if the user adopts the recommendation,
  record the decision (their call — propose, don't self-accept); tick the
  todo; update phase if warranted.
- Report: verdict in two sentences, what it unblocks, suggested next step.

## Rules

- One spike, one question. A second unknown discovered mid-spike becomes a
  new Q-### — levelled and placed per the item-triage skill, so an
  implementation detail met along the way parks instead of interrupting —
  and possibly a new spike, but not added scope.
- Spike code is throwaway by default: it never graduates into `outputs/` or
  production; the verdict and its evidence are the deliverables.
- Never modify anything outside `spikes/<name>/` except the spine-file
  ripples described above.
