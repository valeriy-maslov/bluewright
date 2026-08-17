# Bluewright workspace specification

Single source of truth for the workspace layout, file formats, and resolution
rules. Every bluewright command must follow this spec exactly so that all
commands read and write the same shapes.

## Resolution rules

1. **Workspace** — walk up from the current working directory looking for a
   `workspace.yml`. The nearest one wins; its directory is the workspace root.
   If none is found, STOP and tell the user they are not inside a Bluewright
   workspace — suggest `/bluewright:init <path>` or `cd`-ing into one. Never
   look anywhere else (no global registry, no home-directory state).
2. **Global** — once the workspace is found, `<workspace>/global/` is its
   official, workspace-wide record. There is no further resolution: every
   command that touches global scope reads and writes it directly. It always
   exists once `/bluewright:init` has run.
3. **Active investigation** — if the cwd is inside `<workspace>/<slug>/` and
   that folder has an `investigation.yml`, that is the active investigation.
   Otherwise the command's argument names the slug. With neither, list the
   investigations in the workspace and ask which one (commands that can run
   without one — `/bluewright:ask`, `/bluewright:make-artifact` — instead
   fall back to global-only scope; say so explicitly).
4. **Boundary** — commands must not read or write outside the workspace tree,
   with exactly two exceptions: (a) paths/queries the user put on a watchlist,
   and (b) the target path the user gave to `/bluewright:init`.

## Workspace layout

```
<workspace>/                    # one per product/team; a git repo
  workspace.yml                 # marker + workspace-level config
  KNOWLEDGE.md                  # index of investigations
  global/                       # official, workspace-wide record
    decisions.md                # append-only decision log — same format as an investigation's
    questions.md                # open questions — same format as an investigation's
    todo.md                     # prioritized TODO — same format as an investigation's
    inputs/                     # raw material captured at global scope
    artifacts/                  # cross-investigation artifacts (created on first use)
  <feature-slug>/               # one investigation (kebab-case slug)
    investigation.yml           # status, links, watchlist
    inputs/                     # requirements, samples, diagrams, pasted material
    decisions.md                # append-only decision log
    questions.md                # open questions
    todo.md                     # prioritized TODO
    sync-log.md                 # append-only trail of /sync runs (written only by /sync)
    artifacts/                  # shareable output: .md, .puml, .png, or anything else asked for
```

`global/` and every investigation's `decisions.md` / `questions.md` /
`todo.md` share one format (below) and one ID scheme, but each file numbers
its own `D-`/`Q-`/`T-` sequence independently — the same way two different
investigations already don't share numbering. A promoted entry's ID in
`global/` is therefore unrelated to its ID in the investigation it came
from; the cross-reference between them is a link, not a shared number (see
"Promotion" below).

### artifacts/

The only folder a command writes shareable output into. There is no fixed
filename list — `/bluewright:make-artifact` produces whatever was asked for
(a doc, a diagram, an email draft, a summary, a wiki page, ...) under a
name that describes it. `artifacts/` is the only thing ever handed to
someone outside the investigation; nothing elsewhere may be required to
understand its contents.

## workspace.yml

```yaml
name: acme-platform             # short workspace name
bluewright: "2.0.0"            # plugin version that created / last migrated
                                #   this workspace; used to detect breaking
                                #   format changes and drive future migrations
team: ""                        # optional: owning team/product
created: 2026-08-06
defaults:                       # inherited by every investigation
  jira_project_keys: []         # e.g. [CORE, API]
  confluence_space: ""          # e.g. ENG
  watchlist: []                 # watchlist entries (see shape below)
```

## Watchlist entry shape

Used in `workspace.yml` defaults and per-investigation. An investigation's
effective watchlist is the workspace defaults plus its own entries.

```yaml
- type: repo                    # repo | jira | confluence
  path: ~/src/some-service      # repo: local clone to inspect (git log/diff)
  branch: main                  # repo: branch to track (default main)
  note: "owns the ledger API"   # why this is watched (always recommended)

- type: jira
  jql: "project = CORE AND component = payments"

- type: confluence
  page_id: "123456"
```

## investigation.yml

```yaml
slug: payments-split
title: "Split payment support"
status: active                  # active | closed — set by the user (directly,
                                 # or via /bluewright:capture when the material
                                 # says the investigation is done); no command
                                 # transitions it automatically
created: 2026-08-06
links:
  jira_epic: ""                 # issue key or URL
  confluence: []                # related page URLs/ids
watchlist: []                   # entries specific to this investigation
sync:
  last_run: null                # ISO timestamp, written only by /sync
```

## decisions.md

Append-only log. IDs `D-001, D-002, ...` are sequential and never reused;
a wrong decision is superseded by a new entry, never edited or deleted.
Newest entry at the BOTTOM. This format is identical for `global/decisions.md`
and every investigation's `decisions.md`.

```markdown
# Decisions — <title>

## D-001 — <short imperative title>
- Date: 2026-08-06
- Status: accepted              # proposed | accepted | superseded by D-00X

**Context:** what was true / what forced a choice.
**Decision:** the choice made, one paragraph max.
**Consequences:** what this commits us to; what it rules out.
**Links:** related Q-IDs, inputs, external refs, and — for a decision
  promoted from an investigation — its source, e.g.
  "promoted from payments-split/decisions.md#D-004".
```

## questions.md

IDs `Q-001, ...`, sequential, never reused. Resolved questions stay in the
file with their answer — they are part of the record. Same format for
`global/questions.md` and every investigation's `questions.md`.

```markdown
# Questions — <title>

## Q-001 — <the question, phrased so it can be answered>
- Status: open                  # open | answered | dropped
- Raised: 2026-08-06 (source: /bluewright:capture — or, for a promoted
  question, "promoted from payments-split/questions.md#Q-004")
- Blocks: D-004                 # what cannot proceed until answered

**Answer:** (filled when answered, with date and source)
```

## todo.md

Priority is expressed by section, order within a section matters (top = next).
IDs `T-001, ...` sequential. Finished items move to Done with a date. Same
format for `global/todo.md` and every investigation's `todo.md`.

```markdown
# TODO — <title>

## Now
- [ ] T-003 — confirm ledger API ownership with team X

## Next
- [ ] T-004 — write up the outbox pattern trade-offs (promoted from
  payments-split/todo.md#T-002)

## Later

## Done
- [x] T-001 — collect current requirements docs  (2026-08-06)
```

## Promotion (investigation → global)

`/bluewright:promote` **copies** a decision, question, or TODO from an
investigation into the matching `global/*.md` file; it never moves or edits
the investigation's original entry. The global copy gets the next ID in
`global/`'s own sequence and carries a back-reference to the source, using
the fields the format already has — `Links:` on a decision, the `(source:
...)` slot on a question, a parenthetical on a TODO line — never a new
field. Nothing is invented in the promoted copy: it restates what the
investigation already recorded.

## sync-log.md

Append-only, one section per `/sync` run, newest at the BOTTOM. Written only
by `/sync`. Investigation-scoped only — there is no global sync-log.

```markdown
# Sync log — <title>

## 2026-08-06T14:30:00Z
- repo ledger-service: 4 commits (3 relevant)
- jira "project = CORE...": 2 updated issues
- impact: D-004 weakened → Q-012 raised
- quiet: confluence 123456
```

## KNOWLEDGE.md

The workspace-wide index of investigations; one line per investigation. Keep
it terse — it is an index, not a document. Facts and decisions that recur
across investigations belong in `global/`, not here.

```markdown
# Knowledge index — <workspace name>

## Investigations
- [Split payment support](payments-split/) — status: active; how we split a
  payment across ledgers. Key: D-004 (async ledger API).
```

## Versioning

`workspace.yml` records the plugin version (`bluewright`) that created or
last migrated the workspace. Commands read it when resolving the workspace:

- same version as the installed plugin → proceed;
- older version, same major → proceed, formats are compatible, but mention
  that `/bluewright:migrate` can bring the recorded version fully current;
- older version, different major → stop and say `/bluewright:migrate` is
  required before continuing;
- newer version → stop; the installed plugin is older than the workspace —
  update the plugin.

Only `/bluewright:init` and `/bluewright:migrate` may write this field.

Enforcement is deterministic: the plugin's `UserPromptSubmit` hook
(`hooks/check-workspace-version.py`) runs on every `/bluewright:*` prompt
(except `init` and `migrate` — the latter exists specifically to run
against an out-of-date workspace), compares `bluewright` with the installed
plugin version, and blocks the command on incompatibility. Commands
therefore do not need to re-check versions themselves.

## Migrating from 1.x

`/bluewright:migrate` follows this mapping exactly; it is additive and
renames only — no decision, question, TODO, or input is ever touched.

| 1.x | 2.x |
|---|---|
| `outputs/` (per investigation) | renamed `artifacts/`; no more fixed filenames inside it |
| `investigation.yml`: `phase: frame\|options\|spike\|share\|design` | `status: active` |
| `investigation.yml`: `phase: done` | `status: closed` |
| `spikes/<name>/` | left in place, untouched — no longer part of the managed layout, but its `SPIKE.md`/`VERDICT.md`/code stay as investigation history |
| *(new)* | `global/` scaffolded at the workspace root (same as `/bluewright:init` creates for a new workspace) |

`decisions.md`, `questions.md`, `todo.md`, and `sync-log.md` formats are
unchanged between 1.x and 2.x — nothing about them needs migrating.

## Conventions

- Slugs: kebab-case.
- Dates: `YYYY-MM-DD`; timestamps: ISO-8601.
- `artifacts/` (global or per-investigation) is the only folder ever shared
  with others; nothing elsewhere may be required to understand its contents.
- Cross-investigation and investigation↔global references are relative
  wiki-style links from the workspace root, e.g.
  `payments-split/decisions.md#D-004` or `global/decisions.md#D-012`.
