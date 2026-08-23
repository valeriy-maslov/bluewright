---
description: Produce a shareable artifact — a document, diagram, presentation outline, wiki page, email, summary, anything asked for — from captured global and investigation information
argument-hint: [what to produce, optional]
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, Skill, AskUserQuestion
---

Turn what's been captured into something a colleague can receive. Unlike
the old fixed-output commands this replaces, there's no fixed template
list — you produce whatever shape the user actually asked for, grounded in
`global/` and the active investigation's record.

First read the spec at `${CLAUDE_PLUGIN_ROOT}/docs/spec.md` and follow its
formats and resolution rules exactly, especially the `artifacts/` section.

Ask: `$ARGUMENTS`

## Steps

1. **Resolve** the workspace per the spec, and the active investigation if
   the cwd is inside one or the user names one. No active investigation →
   global-only scope; artifacts land in `global/artifacts/` instead of an
   investigation's.
2. **Clarify what's being asked for, in prose** if `$ARGUMENTS` doesn't
   already make it clear: artifact type (doc, diagram, presentation
   outline, wiki page, email draft, summary, ...), audience, and the
   topic/scope to pull from. This is free-form judgment, not a
   multiple-choice moment — don't force `AskUserQuestion` on it.
3. **Gather source material**: `global/decisions.md`, `global/questions.md`,
   `global/todo.md`, relevant `global/inputs/`, and — if an investigation is
   active — its own equivalents, filtered to the requested topic. Note
   plainly what's thin or missing rather than inventing to paper over gaps.
4. **Reach for a template only when the shape calls for one:**
   - a solution-design-shaped document → load the `bluewright:solution-design`
     skill for the template and quality bar;
   - a diagram → load the `bluewright:plantuml-conventions` skill; render
     via a local `plantuml` CLI if installed, else the docker one-shot
     (`docker run --rm plantuml/plantuml`), else report it unrendered
     rather than skipping it silently.
   Anything else (an email, a summary, a wiki page, a presentation outline)
   has no fixed template — write it to fit the ask.
5. **Write the artifact** to `<investigation>/artifacts/<kebab-name>.<ext>`
   (or `global/artifacts/` for a global-only run). Never silently overwrite
   an existing artifact with the same name — a bounded choice, so use
   `AskUserQuestion` (`Overwrite` / `Use a different name`).
6. **Trace what you can, flag what you can't.** Every non-trivial claim
   should point back to a `D-###`/`Q-###`/`T-###` or an `inputs/` source
   where the record actually supports it. Where it's silent, say so as an
   open item in the artifact itself (not a self-filed question) and mention
   it in your report — the user decides whether to `/bluewright:capture` it
   first and regenerate, or ship it as-is.
7. **Report** one screen: where the artifact landed, what it drew on
   (counts: decisions, questions, inputs consulted), and anything flagged
   thin.

## Rules

- Reads `global/` and investigation spine files; never edits
  `decisions.md`, `questions.md`, or `todo.md` — this command only writes
  into `artifacts/`.
- Re-running for the same ask regenerates the artifact; it never rewrites
  history in the spine files.
- Touch nothing outside the workspace tree.
