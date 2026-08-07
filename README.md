# Bluewright

[![Validate](https://github.com/valeriy-maslov/bluewright/actions/workflows/validate.yml/badge.svg?branch=master)](https://github.com/valeriy-maslov/bluewright/actions/workflows/validate.yml)

A [Claude Code](https://claude.com/claude-code) plugin for **feature investigations** — the
work that happens *before* implementation: figuring out what's actually being asked, what
already exists, which approaches are viable, which one wins, and why.

Bluewright gives that work a home. One folder per investigation holds your inputs, your
decisions, your open questions, your to-do list, your experiments, and the polished
artifacts you hand to a team. Nothing lives in Claude's memory or in hidden state —
everything is plain Markdown and YAML in a git repository you own.

## Install

```
/plugin marketplace add valeriy-maslov/bluewright
/plugin install bluewright@bluewright
```

Restart Claude Code (or start a new session) so the commands, agents, and skills load.

## Getting started

```
/bluewright:init ~/work/my-team        # once per product/team
cd ~/work/my-team
/bluewright:new payments-split         # once per feature
```

Bluewright finds your workspace by walking up from the directory you're in — the way git
finds a repository. Run commands from inside the workspace (or inside a specific
investigation) and they know where they are. There is no global registry to configure.

Then drop whatever you have into `inputs/` — requirement docs, meeting notes, diagrams,
sample payloads — and run `/bluewright:brief`.

## Commands

**Setting up — once each**

| Command | What it does |
|---|---|
| `/bluewright:init <path>` | Creates a workspace: `workspace.yml`, `KNOWLEDGE.md`, git init. Asks for team defaults; refuses to nest inside another workspace. |
| `/bluewright:new <slug>` | Creates one investigation: the folder structure, the four living files, and your kickoff answers preserved in `inputs/00-intake.md`. |

**Every day**

| Command | What it does |
|---|---|
| `/bluewright:status` | One screen: phase, next tasks, open questions (blocking first), latest decisions, sync freshness. Read-only. |
| `/bluewright:capture` | The inbox. Paste feedback, a Slack thread, meeting notes — it saves the raw text and routes each item to a decision, question, or task. Never overrules an accepted decision by itself. |

**Analysis**

| Command | What it does |
|---|---|
| `/bluewright:brief` | Requirements analysis: digests `inputs/`, surveys watched systems, writes `outputs/brief.md`, seeds questions from the gaps. |
| `/bluewright:options` | Option comparison: candidates and criteria agreed with you first, parallel research per candidate, scored matrix in `outputs/options.md`. |
| `/bluewright:spike <name>` | Time-boxed proof of concept answering exactly one question — the one place where installing and running things is allowed. Always ends in a `VERDICT.md`. |

**Watching the outside world**

| Command | What it does |
|---|---|
| `/bluewright:sync` | Checks every watchlist entry for changes since the last run and answers the question that matters: *which of my assumptions moved?* Runs unattended, so you can schedule it. |

**Delivering**

| Command | What it does |
|---|---|
| `/bluewright:publish` | Makes `outputs/` shareable: renders diagrams, verifies nothing links outside the folder, marks stale artifacts honestly. |
| `/bluewright:design` | The finale: synthesizes `outputs/design.md` from your decisions, option analysis, and spike verdicts — refusing politely if blocking questions are still open. |

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
└── skills/               # solution-design template, PlantUML conventions, decision entry
```

## Versioning

Each workspace records the plugin version that created it in `workspace.yml`:

```yaml
bluewright: "1.0.0"
```

A `UserPromptSubmit` hook compares that against the installed plugin on every
`/bluewright:*` command and blocks when the workspace is newer than the plugin, or when a
major-version format change needs a migration. See
[`docs/spec.md`](docs/spec.md) § Versioning.

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
[`PRIVACY.md`](PRIVACY.md) walks through every moving part, including the two components
that can reach the internet and when they do.

## Security

Found something that looks like a security problem? Please report it privately — through
[GitHub](https://github.com/valeriy-maslov/bluewright/security/advisories/new) or by email —
rather than opening an issue. [`SECURITY.md`](SECURITY.md) covers what counts, what is
deliberate (`/bluewright:spike` runs code on purpose), and what to expect after you report.

## License

[MIT](LICENSE) © Valeriy Maslov
