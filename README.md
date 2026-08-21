# Bluewright

[![Validate](https://github.com/valeriy-maslov/bluewright/actions/workflows/validate.yml/badge.svg?branch=master)](https://github.com/valeriy-maslov/bluewright/actions/workflows/validate.yml)

A [Claude Code](https://claude.com/claude-code) plugin for **capturing what a team knows** —
decisions, open questions, and TODOs, at two tiers: an official, workspace-wide record and
a per-investigation one that can graduate into it. Once something is captured, ask
questions about it or turn it into whatever artifact you need. Nothing lives in Claude's
memory or in hidden state — everything is plain Markdown and YAML in a git repository you
own.

## Install

```
/plugin marketplace add valeriy-maslov/bluewright
/plugin install bluewright@bluewright
```

Restart Claude Code (or start a new session) so the commands, agents, and skills load.

## Update

```
/plugin marketplace update bluewright
/plugin update bluewright@bluewright
```

The first command refreshes the marketplace listing from this repository; the second
installs the newer version if one is available. Restart Claude Code (or start a new
session) afterward, same as a fresh install. Check what's currently installed with
`/plugin list`.

Updates are version-gated: `.claude-plugin/plugin.json` pins an explicit `version`, and
`/plugin update` is a no-op until that number changes upstream — see
[`CHANGELOG.md`](CHANGELOG.md) for what changed in each release. If the release is a major
version bump, run `/bluewright:migrate` once per existing workspace afterward; see
Versioning below.

## Getting started

```
/bluewright:init ~/work/my-team        # once per product/team
cd ~/work/my-team
/bluewright:new payments-split         # once per feature
```

Bluewright finds your workspace by walking up from the directory you're in — the way git
finds a repository. Run commands from inside the workspace (or inside a specific
investigation) and they know where they are. There is no global registry to configure.

Then capture whatever you have — paste it, point at a file, or just talk — with
`/bluewright:capture-global` for anything workspace-wide and official, or
`/bluewright:capture` for anything specific to the investigation you're in. When you've
captured enough, `/bluewright:ask` to explore it or `/bluewright:make-artifact` to turn it
into something you can hand to someone.

## Commands

**Setting up — once each**

| Command | What it does |
|---|---|
| `/bluewright:init <path>` | Creates a workspace: `workspace.yml`, `KNOWLEDGE.md`, `global/`, git init. Asks for team defaults; refuses to nest inside another workspace. |
| `/bluewright:new <slug>` | Creates one investigation: the folder structure, the four living files, and your kickoff answers preserved in `inputs/00-intake.md`. |
| `/bluewright:migrate` | Brings an older workspace's on-disk format up to date with the installed plugin (e.g. scaffolding `global/`, renaming `outputs/` to `artifacts/`). Additive and renames only — never deletes data. The version hook points here whenever it blocks a command over a format mismatch. |

**Capturing**

| Command | What it does |
|---|---|
| `/bluewright:capture-global` | The inbox for the workspace's official record. Paste feedback, notes, anything workspace-wide — saves the raw text, guides you through which questions/TODOs are actually worth tracking, and never overrules an accepted decision by itself. |
| `/bluewright:capture` | The same inbox, scoped to the active investigation — not yet official, but promotable. |
| `/bluewright:promote` | Copies selected decisions/questions/TODOs from an investigation into `global/`, with a back-reference to the source. Never edits the investigation's original entry. |

**Every day**

| Command | What it does |
|---|---|
| `/bluewright:status` | One screen: a global-record glance, status, next tasks, open questions (blocking first), latest decisions, sync freshness. Read-only. |
| `/bluewright:ask` | Interactively analyze what's captured — global and the active investigation — without changing anything. Cites what it's drawing on; says "not captured yet" rather than inventing. |
| `/bluewright:make-artifact` | Turns captured information into whatever you ask for — a doc, a diagram, a wiki page, an email, a summary, a presentation outline, anything — grounded in the record, flagging what's thin instead of inventing to fill it. |

**Watching the outside world**

| Command | What it does |
|---|---|
| `/bluewright:sync` | Checks every watchlist entry for changes since the last run and answers the question that matters: *which of my assumptions moved?* Runs unattended, so you can schedule it. |

## Documentation

- **[User manual](docs/manual.html)** — the guided tour, with a worked example.
- **[Workspace specification](docs/spec.md)** — the on-disk contract: folder layout, file
  formats, ID schemes, and versioning rules that every command follows.
- **[Changelog](CHANGELOG.md)** — what changed in each release, and whether it touches
  anything on disk.

## What's in the plugin

```
bluewright/
├── .claude-plugin/
│   ├── plugin.json       # plugin manifest
│   └── marketplace.json  # so this repo can be added as a marketplace
├── agents/               # read-only subagents dispatched by the commands
├── commands/             # the /bluewright:* slash commands
├── docs/                 # user manual + workspace specification
├── hooks/                # plugin/workspace version-compatibility check
└── skills/               # decision entry, question/TODO triage, solution-design template, PlantUML conventions
```

## Versioning

Each workspace records the plugin version that created it in `workspace.yml`:

```yaml
bluewright: "3.0.0"
```

A `UserPromptSubmit` hook compares that against the installed plugin on every
`/bluewright:*` command and blocks when the workspace is newer than the plugin, or when a
major-version format change needs a migration. `/bluewright:init` and `/bluewright:migrate`
are exempt — migration has to stay reachable in the workspaces the block applies to. See
[`docs/spec.md`](docs/spec.md) § Versioning and § Migrating to 3.x.

Upgrading across a major version means running `/bluewright:migrate` once per workspace. It
converts every investigation in place, preserves every `Q-###` and `T-###`, requires a clean
git tree, and never commits — so `git diff` is the review and `git revert` is the undo.

## Local development

Install from a checkout instead of from GitHub:

```
/plugin marketplace add /path/to/bluewright
/plugin install bluewright@bluewright
```

Validate the manifests before committing:

```bash
claude plugin validate . --strict
```

Reinstalling is version-gated — bump `version` in `.claude-plugin/plugin.json` before
`/plugin update bluewright@bluewright` picks up your changes.

## Data handling

Bluewright collects nothing: no backend, no telemetry, no network calls of its own. Your
investigations are plain files in your own git repository, and the version hook reads each
prompt only to test whether it starts with `/bluewright:` — it stores and sends nothing.
[`PRIVACY.md`](PRIVACY.md) walks through every moving part, including the one command that
reaches the internet (`/bluewright:sync`, and only for watchlist entries you configured).

## Security

Found something that looks like a security problem? Please report it privately — through
[GitHub](https://github.com/valeriy-maslov/bluewright/security/advisories/new) or by email —
rather than opening an issue. [`SECURITY.md`](SECURITY.md) covers what counts and what to
expect after you report.

## License

[MIT](LICENSE) © Valeriy Maslov
