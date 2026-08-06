---
description: Bootstrap a new investigation (spine files, inputs/, spikes/, outputs/) in the current workspace
argument-hint: [feature-slug]
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, AskUserQuestion
---

Bootstrap a new **investigation** inside the current Bluewright workspace.

First read the spec at `${CLAUDE_PLUGIN_ROOT}/docs/spec.md` and follow its
formats and resolution rules exactly.

Requested slug: `$ARGUMENTS`

## Steps

1. **Resolve the workspace** per the spec (walk up from cwd to the nearest
   `workspace.yml`). If none is found, stop and explain, suggesting
   `/bluewright:init <path>` or `cd`-ing into an existing workspace.
2. **Validate the slug.** Kebab-case, short, descriptive. If no argument was
   given, ask for one. If `<workspace>/<slug>/` already exists, stop and say
   so.
3. **Interview, briefly — in plain text.** Ask in one conversational
   message for:
   - title (one line) and the goal — what question must this investigation
     answer in the end;
   - Jira epic / driving ticket (if any);
   - related Confluence pages (if any);
   - repos or systems to watch beyond the workspace defaults.
   Everything except the title is optional. These are free-form answers —
   do NOT use AskUserQuestion for them (it requires 2–4 predefined options
   per question and rejects the call otherwise); just ask in prose. Reserve
   AskUserQuestion for genuine multiple-choice moments (e.g. picking among
   existing investigations).
4. **Create the investigation** per the spec:
   - `investigation.yml` — phase `frame`, today's date, links and watchlist
     from the interview (workspace defaults are NOT copied in; they are merged
     at read time);
   - `decisions.md`, `questions.md`, `todo.md` — seeded with their headers,
     empty sections, and no entries;
   - `inputs/00-intake.md` — the goal statement and everything else the user
     provided during the interview, verbatim, so nothing said at creation
     time is lost;
   - `inputs/`, `spikes/`, `outputs/` folders (add `.gitkeep` to the empty
     ones).
5. **Seed `todo.md`** with the obvious first tasks in **Now**, e.g.
   `T-001 — collect requirements and materials into inputs/` and
   `T-002 — run /bluewright:brief`. If the interview surfaced an unknown
   worth deciding, add it to `questions.md` as `Q-001` instead of losing it.
6. **Index.** Append the investigation's line to the workspace `KNOWLEDGE.md`
   under **Investigations**, per the spec format.
7. **Report.** Show the created tree and the immediate next steps: drop
   materials into `inputs/`, then run `/bluewright:brief`.

## Rules

- Touch nothing outside the workspace tree.
- Never overwrite existing files.
- Do not invent content: requirements analysis belongs to `/bluewright:brief`,
  not here. This command only creates the container and records what the user
  said.
