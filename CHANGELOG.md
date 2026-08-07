# Changelog

All notable changes to Bluewright are recorded here. The format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and the project follows
[semantic versioning](https://semver.org/) — see
[CONTRIBUTING.md](CONTRIBUTING.md) § Versioning for what earns a major, minor, or patch
bump.

Because a workspace records the plugin version that created it, entries call out
explicitly when a release changes anything on disk.

## [Unreleased]

Nothing yet.

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
