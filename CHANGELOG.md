# Changelog

All notable changes to Bluewright are recorded here. The format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and the project follows
[semantic versioning](https://semver.org/) — see
[CONTRIBUTING.md](CONTRIBUTING.md) § Versioning for what earns a major, minor, or patch
bump.

Because a workspace records the plugin version that created it, entries call out
explicitly when a release changes anything on disk.

## [Unreleased]

## [4.0.0] — 2026-08-23

**This release changes the on-disk workspace format.**

### Changed

- Watchlist entries and links are now tool-agnostic. `workspace.yml`'s
  `defaults.jira_project_keys`/`defaults.confluence_space` and
  `investigation.yml`'s `links.jira_epic`/`links.confluence` are replaced by
  a generic `watchlist` (`type: external` with free-text `label`/`query`)
  and a generic `links: []` list of free-text references — Bluewright
  bundles no integration with any specific issue tracker or wiki.
- `/bluewright:sync` no longer special-cases Jira/Confluence MCP tools for
  external entries; it searches available MCP tools at run time for one
  that plausibly matches an entry's `label`/`query`, and skips the entry
  with a reason if none is found.
- `/bluewright:migrate` converts pre-`4.0.0` `jira`/`confluence` fields and
  watchlist entries to the generic shape — additive, nothing is deleted.

### Removed

- The hardcoded `jira`/`confluence` watchlist entry types (`jql`, `page_id`
  fields) — superseded by the generic `external` type above.

## [3.0.0] — 2026-08-17

**This release changes the on-disk workspace format.** It also replaces the
altitude/parking mechanism `2.0.0` shipped days earlier with a different answer to the same
problem — see the note under Removed.

### Added

- **`global/` tier**: a workspace-wide, official record (`decisions.md`, `questions.md`,
  `todo.md`, `inputs/`, `artifacts/`) alongside every investigation's own, not-yet-official
  one. Created by `/bluewright:init`.
- `/bluewright:capture-global` — the triage inbox for `global/`, mirroring
  `/bluewright:capture` but workspace-scoped.
- `/bluewright:promote` — copies selected decisions/questions/TODOs from an investigation
  into `global/`, with a back-reference to the source; never edits or removes the
  investigation's original entry.
- `/bluewright:ask` — read-only, interactive analysis over the captured record (global +
  active investigation), citing sources and saying "not captured yet" rather than
  inventing.
- `/bluewright:make-artifact` — produces any shareable artifact (doc, diagram, wiki page,
  email, summary, presentation outline, ...) from the captured record, replacing the fixed
  brief/options/design/tickets outputs with an open-ended one.
- `question-todo-triage` skill: a guided, deduped conversation for turning captured
  material into `questions.md`/`todo.md` entries, used by both capture commands — replaces
  auto-filing every inferable question or TODO.
- `/bluewright:migrate` — brings an older workspace's on-disk format up to date (scaffolds
  `global/`, renames `outputs/` to `artifacts/`, converts `phase` to `status` per
  investigation, and flattens `2.0.0`'s `Active`/`Parked`/`Closed` structure back to a plain
  list where applicable). Additive and renames only, never deletes data; exempt from the
  version hook's block for exactly this reason; requires a clean git tree and never commits,
  so `git diff`/`git revert` are the review and undo. See `docs/spec.md` § Migrating to 3.x.
- Changelog-driven releases: pushing a new version section to `master` tags the commit
  and publishes a GitHub release with that section as the notes
  (`.github/workflows/release.yml`). Repository tooling only — nothing changes for
  installed plugins or existing workspaces.
- Privacy and data-handling statement ([`PRIVACY.md`](PRIVACY.md)): what the plugin
  collects (nothing), what the `UserPromptSubmit` hook does with each prompt, and which
  components can reach the network. Documentation only — nothing changes for installed
  plugins or existing workspaces.
- Security policy ([`SECURITY.md`](SECURITY.md)) with private vulnerability reporting
  enabled on the repository: how to report, what counts as a vulnerability in a plugin made
  of prompts, and what is deliberate. Documentation only — nothing changes for installed
  plugins or existing workspaces.

### Changed

- **Workspace format, breaking**: `investigation.yml`'s `phase` field is replaced by
  `status: active | closed`; `outputs/` is renamed `artifacts/` and no longer has a fixed
  filename list; `spikes/` is dropped; the FR/NFR/C requirements-ID scheme is dropped (it
  only existed to serve `/bluewright:brief`); `questions.md`/`todo.md` drop `2.0.0`'s
  `Active`/`Parked`/`Closed` sections and `Level:` field in favor of a single flat list —
  see Removed.
- `/bluewright:capture` now facilitates questions/TODOs through the
  `question-todo-triage` skill instead of filing every item it can infer, and its
  contradiction check now also compares against accepted `global/decisions.md` entries.
- `/bluewright:status` drops the phase/design-gate and spike-verdict flags, adds a
  one-line global-record glance, and its staleness flag now points at
  `/bluewright:make-artifact`.
- `decision-entry`, `solution-design`, and `plantuml-conventions` skills are reframed:
  `decision-entry` now targets either `global/` or an investigation's `decisions.md`;
  `solution-design` and `plantuml-conventions` are optional templates
  `/bluewright:make-artifact` loads on request, rather than being tied to a specific
  removed command.
- The version hook (`hooks/check-workspace-version.py`) now exempts `/bluewright:migrate`
  alongside `/bluewright:init`, and names the command in its messages.

### Removed

- **Commands**: `/bluewright:brief`, `/bluewright:options`, `/bluewright:spike`,
  `/bluewright:publish`, `/bluewright:design` — replaced by capture-first workflow plus
  `/bluewright:ask` and `/bluewright:make-artifact`.
- **Agents**: `requirements-analyst`, `system-surveyor`, `option-scout`, `doc-builder` —
  they existed only to serve the removed commands. `impact-assessor` (used by
  `/bluewright:sync`) stays.
- **`2.0.0`'s altitude/parking mechanism**: `/bluewright:groom`, the `item-triage` skill,
  the `Level` field, and the `Active`/`Parked`/`Closed` question/TODO sections. That release
  solved the same problem this one does — an investigation accumulating more questions and
  TODOs than anyone could act on — by classifying and hiding items after the fact. This
  release solves it earlier instead, at capture time, via `question-todo-triage`'s guided
  conversation, and removes the after-the-fact machinery rather than running both. Nothing
  from a `2.0.0` workspace is lost: `/bluewright:migrate` folds `Active` and `Parked` entries
  back into the flat list.

## [2.0.0] — 2026-08-07

**This release changes files on disk and requires a migration.** Run
`/bluewright:migrate` in each existing workspace; every other `/bluewright:*` command is
blocked until you do (the version hook enforces this, and exempts `migrate` itself so it
stays reachable). The migration preserves every `Q-###` and `T-###` — nothing is renumbered
or deleted.

### Added

- **Altitude** — every question and TODO now carries a `Level` (`frame`, `options`,
  `design`, `build`): the earliest phase at which answering it changes anything. Items at or
  above the investigation's current phase are active; the rest are parked. Parking defers,
  it never discards — `/bluewright:design` promotes the `design`-level items when it runs
  and drafts tickets from the `build`-level ones. Defined in
  [`docs/spec.md`](docs/spec.md) § Altitude.
- **`bluewright:item-triage` skill** — the single place that defines how an item earns a
  level, how it is deduplicated against what already exists, when several items are rolled
  up into one, and why reports count parked items instead of listing them. Every command
  that writes `questions.md` or `todo.md` loads it.
- **`/bluewright:groom`** — consolidates one investigation on demand: re-levels
  automatically, then proposes merges in batches for your confirmation. Nothing is deleted;
  absorbed entries move to `Closed` with `Status: merged`.
- **`/bluewright:migrate`** — converts a whole workspace to the installed plugin's format,
  runs the groom pass per investigation, and records the new version in `workspace.yml`.
  Requires a clean git tree, and never commits.

### Changed

- **Workspace format (breaking)** — `questions.md` now has `Active` / `Parked` / `Closed`
  sections with entries at `###`, a `Level:` field, and an accumulating `**Evidence:**`
  block; `Status` gains `parked` and `merged`. `todo.md` gains a `Parked` section, and items
  carry `(level: …)` in place of the old `(phase: …)` suffix.
- **Writers stop appending one-for-one.** `/bluewright:capture` deduplicates before
  allocating an ID — an existing question gains a dated evidence line instead of a twin —
  and levels each item from its content rather than asking. `/bluewright:brief` clusters the
  requirements analyst's conflicts, ambiguities, and gaps by the decision each bears on: one
  question per decision, not one per finding. `/bluewright:options`, `/bluewright:spike`,
  `/bluewright:sync`, `/bluewright:new`, and the `decision-entry` skill do the same.
- **`requirements-analyst`** groups its findings by decision and returns a `level` on each;
  **`impact-assessor`** returns a `level` on each hit.
- **`/bluewright:status`** renders active items only, summarises parked ones as counts by
  level, and flags an active list that has outgrown a glance — pointing at
  `/bluewright:groom`. Still strictly read-only.
- **`/bluewright:design`** promotes parked `design`-level items into the active set before
  writing, and sources ticket material from the `build`-level ones.
- The version hook (`hooks/check-workspace-version.py`) now exempts `/bluewright:migrate`
  alongside `/bluewright:init`, and names the command in its messages.

### Fixed

- Questions and TODOs no longer grow without bound. Previously eight writers appended to
  these two files with no altitude test, no deduplication, and no retirement rule, so a few
  dozen captures could bury an investigation in fine-grained items it had no way to act on.

## [1.0.0] — 2026-08-06

First release.

### Added

- **Commands** — `/bluewright:init` and `/bluewright:new` for setup; `/bluewright:status`
  and `/bluewright:capture` for daily use; `/bluewright:brief`, `/bluewright:options`, and
  `/bluewright:spike` for analysis; `/bluewright:sync` for watchlist drift; and
  `/bluewright:publish` and `/bluewright:design` for delivery.
- **Agents** — read-only subagents the commands dispatch: `requirements-analyst`,
  `system-surveyor`, `option-scout`, `impact-assessor`, `doc-builder`.
- **Skills** — `solution-design` (the design template and quality bar),
  `plantuml-conventions` (diagram style), `decision-entry` (how a decision is recorded).
- **Workspace format** — one folder per investigation with `inputs/`, `outputs/`, and the
  four living files, defined by [`docs/spec.md`](docs/spec.md).
- **Version hook** — `hooks/check-workspace-version.py` runs on every `/bluewright:*`
  prompt and blocks when the workspace is newer than the installed plugin or a major
  format gap needs a migration.
- **Docs** — the [user manual](docs/manual.html) and the
  [workspace specification](docs/spec.md).

[Unreleased]: https://github.com/valeriy-maslov/bluewright/compare/v4.0.0...HEAD
[4.0.0]: https://github.com/valeriy-maslov/bluewright/compare/v3.0.0...v4.0.0
[3.0.0]: https://github.com/valeriy-maslov/bluewright/compare/v2.0.0...v3.0.0
[2.0.0]: https://github.com/valeriy-maslov/bluewright/compare/v1.0.0...v2.0.0
[1.0.0]: https://github.com/valeriy-maslov/bluewright/releases/tag/v1.0.0
