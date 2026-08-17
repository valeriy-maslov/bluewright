# Changelog

All notable changes to Bluewright are recorded here. The format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and the project follows
[semantic versioning](https://semver.org/) — see
[CONTRIBUTING.md](CONTRIBUTING.md) § Versioning for what earns a major, minor, or patch
bump.

Because a workspace records the plugin version that created it, entries call out
explicitly when a release changes anything on disk.

## [Unreleased]

**This release changes the on-disk workspace format** — see below. Requires the major
version bump this section will carry when it's released as `2.0.0`.

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
- `/bluewright:migrate` — brings a 1.x workspace's on-disk format up to date (scaffolds
  `global/`, renames `outputs/` to `artifacts/`, converts `phase` to `status` per
  investigation). Additive and renames only, never deletes data; exempt from the version
  hook's block for exactly this reason. See `docs/spec.md` § Migrating from 1.x.
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
  only existed to serve `/bluewright:brief`).
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

### Removed

- **Commands**: `/bluewright:brief`, `/bluewright:options`, `/bluewright:spike`,
  `/bluewright:publish`, `/bluewright:design` — replaced by capture-first workflow plus
  `/bluewright:ask` and `/bluewright:make-artifact`.
- **Agents**: `requirements-analyst`, `system-surveyor`, `option-scout`, `doc-builder` —
  they existed only to serve the removed commands. `impact-assessor` (used by
  `/bluewright:sync`) stays.

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

[Unreleased]: https://github.com/valeriy-maslov/bluewright/compare/v1.0.0...HEAD
[1.0.0]: https://github.com/valeriy-maslov/bluewright/releases/tag/v1.0.0
