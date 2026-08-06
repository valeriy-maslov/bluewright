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
2. **Active investigation** — if the cwd is inside `<workspace>/<slug>/` and
   that folder has an `investigation.yml`, that is the active investigation.
   Otherwise the command's argument names the slug. With neither, list the
   investigations in the workspace and ask which one.
3. **Boundary** — commands must not read or write outside the workspace tree,
   with exactly two exceptions: (a) paths/queries the user put on a watchlist,
   and (b) the target path the user gave to `/bluewright:init`.

## Workspace layout

```
<workspace>/                    # one per product/team; a git repo
  workspace.yml                 # marker + workspace-level config
  KNOWLEDGE.md                  # cross-investigation index
  <feature-slug>/               # one investigation (kebab-case slug)
    investigation.yml           # state, links, watchlist
    inputs/                     # requirements, samples, diagrams, pasted material
    decisions.md                # append-only decision log
    questions.md                # open questions
    todo.md                     # prioritized TODO
    sync-log.md                 # append-only trail of /sync runs (written only by /sync)
    spikes/<spike-name>/        # each PoC: code + SPIKE.md (goal) + VERDICT.md (outcome)
    outputs/                    # the ONLY shareable surface: .md, .puml, .png
```

### Standard artifacts in outputs/

Commands write shareable artifacts under fixed names, so every investigation
looks the same:

- `outputs/brief.md` — requirements brief (written by `/brief`; derived —
  regenerating is fine, but FR/NFR/C IDs referenced elsewhere are permanent);
- `outputs/options.md` — option comparison and recommendation (written by
  `/options`; same regeneration rule);
- `outputs/design.md` — the solution design (written by `/design`);
- `outputs/tickets.md` — draft implementation tickets (written by `/design`
  on request);
- `outputs/README.md` — reading-order index with staleness flags (written
  by `/publish`);
- `outputs/*.puml` with the rendered `.png` next to each (via `/publish`).

## workspace.yml

```yaml
name: acme-platform             # short workspace name
bluewright: "1.0.0"            # plugin version that created / last migrated
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
phase: frame                    # frame | options | spike | share | design | done
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
Newest entry at the BOTTOM.

```markdown
# Decisions — <title>

## D-001 — <short imperative title>
- Date: 2026-08-06
- Status: accepted              # proposed | accepted | superseded by D-00X
- Phase: options                # phase it was made in

**Context:** what was true / what forced a choice.
**Decision:** the choice made, one paragraph max.
**Consequences:** what this commits us to; what it rules out.
**Links:** related Q-IDs, spike verdicts, inputs, external refs.
```

## questions.md

IDs `Q-001, ...`, sequential, never reused. Resolved questions stay in the
file with their answer — they are part of the record.

```markdown
# Questions — <title>

## Q-001 — <the question, phrased so it can be answered>
- Status: open                  # open | answered | dropped
- Raised: 2026-08-06 (source: /brief gap analysis)
- Blocks: D-004, design         # what cannot proceed until answered

**Answer:** (filled when answered, with date and source)
```

## todo.md

Priority is expressed by section, order within a section matters (top = next).
IDs `T-001, ...` sequential. Finished items move to Done with a date.

```markdown
# TODO — <title>

## Now
- [ ] T-003 — confirm ledger API ownership with team X  (phase: frame)

## Next
- [ ] T-004 — spike: kafka message ordering  (phase: spike)

## Later

## Done
- [x] T-001 — collect current requirements docs  (2026-08-06)
```

## Spike files

`spikes/<name>/SPIKE.md` is written when the spike is scaffolded; `VERDICT.md`
only when it concludes — a spike folder without a `VERDICT.md` is by
definition still open.

```markdown
# SPIKE.md
# Spike — <name>
- Question: Q-00X — <the unknown this spike settles>
- Success criteria: <what result would prove/disprove it>
- Time-box: <e.g. 1 day>
- Started: 2026-08-06
```

```markdown
# VERDICT.md
# Verdict — <name>
- Concluded: 2026-08-07
- Result: proven | disproven | inconclusive

**What was tried:** ...
**Evidence:** measurements, output, file refs inside this spike folder.
**Recommendation:** what this means for the investigation (feeds a D-entry).
```

## sync-log.md

Append-only, one section per `/sync` run, newest at the BOTTOM. Written only
by `/sync`.

```markdown
# Sync log — <title>

## 2026-08-06T14:30:00Z
- repo ledger-service: 4 commits (3 relevant)
- jira "project = CORE...": 2 updated issues
- impact: D-004 weakened → Q-012 raised; NFR-3 informed
- quiet: confluence 123456
```

## KNOWLEDGE.md

The workspace-wide index; one line per investigation plus optional notes on
systems that recur across investigations. Keep it terse — it is an index,
not a document.

```markdown
# Knowledge index — <workspace name>

## Investigations
- [Split payment support](payments-split/) — phase: options; how we split a
  payment across ledgers. Key: D-004 (async ledger API).

## Systems
- **ledger-service** — owned by team X; async API since 2026-07; see
  payments-split/decisions.md#D-004.
```

## Versioning

`workspace.yml` records the plugin version (`bluewright`) that created or
last migrated the workspace. Commands read it when resolving the workspace:

- same version as the installed plugin → proceed;
- older version → proceed if formats are compatible, but mention that a
  future `/bluewright:migrate` can bring the workspace up to date; if the
  spec has had a breaking change since that version, stop and say migration
  is required before continuing;
- newer version → stop; the installed plugin is older than the workspace —
  update the plugin.

Only `/bluewright:init` (and a future migrate command) may write this field.

Enforcement is deterministic: the plugin's `UserPromptSubmit` hook
(`hooks/check-workspace-version.py`) runs on every `/bluewright:*` prompt
(except `init`), compares `bluewright` with the installed plugin version, and
blocks the command on incompatibility. Commands therefore do not need to
re-check versions themselves.

## Conventions

- Slugs, spike names: kebab-case.
- Dates: `YYYY-MM-DD`; timestamps: ISO-8601.
- `outputs/` is the only folder ever shared with others; nothing elsewhere may
  be required to understand its contents.
- Cross-investigation references are relative wiki-style links from the
  workspace root, e.g. `payments-split/decisions.md#D-004`.
