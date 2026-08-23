# Privacy and data handling

Bluewright collects nothing. There is no backend, no telemetry, no analytics, no account,
and no phone-home of any kind. Nothing you do with this plugin is transmitted anywhere by
this plugin.

That is easy to claim and hard to trust, so the rest of this document says exactly what
each moving part touches.

## Where your data lives

In a git repository you own. An investigation is plain Markdown and YAML in a folder on
your disk: your inputs, decisions, questions, tasks, and outputs, all readable in any text
editor.

Bluewright keeps no state outside that tree. Commands find your workspace by walking up
from the current directory looking for `workspace.yml` — there is no global registry, no
home-directory config, no database, no cache. Commands do not read or write outside the
workspace, with two exceptions you set yourself: paths you put on a watchlist, and the
target directory you hand to `/bluewright:init`. See
[`docs/spec.md`](docs/spec.md) § Resolution rules.

## The prompt hook

This is the part worth scrutinising, so here it is in full.

Bluewright installs one `UserPromptSubmit` hook,
[`hooks/check-workspace-version.py`](hooks/check-workspace-version.py). Claude Code runs it
**on every prompt you type** while the plugin is enabled, and hands it the prompt text.
Its entire job is to compare two version strings.

What it does with your prompt: matches it against `^\s*/bluewright:` and stops immediately
if that fails. It does not store the prompt, log it, hash it, count it, or send it
anywhere.

When the prompt *is* a Bluewright command, the hook reads exactly two files — the
`bluewright:` line of your `workspace.yml`, and the plugin's own `plugin.json` — compares
the two versions, and either allows the prompt or blocks it with an explanation. It writes
no files, creates no directories, opens no network connections, and executes nothing. Its
only output is a note in your session.

It is a single file of about 120 lines, importing nothing beyond `json`, `os`, `re`, and
`sys`. Reading it takes a minute, and that is the best assurance this document can offer.

## Network access

Bluewright makes no network calls of its own. It bundles no MCP server and holds no
credentials for anything. No command reaches the general internet by default — none of the
bundled commands or agents carries `WebFetch`/`WebSearch` in its tool list.

The one command that touches the network is `/bluewright:sync`, and only for watchlist
entries you configured. Repository entries are local clones it inspects with git. `external`
entries (an issue tracker query, a wiki page, or anything else you point it at) use
whichever MCP tools **you have connected yourself** that plausibly match the entry; Bluewright
bundles no integration with any specific tool. If nothing matches, the entry is marked
`skipped: no tool found` and nothing is contacted. It runs only because you invoked it (or
scheduled it).

## What you put in

`inputs/` and `/bluewright:capture` store what you give them, verbatim, in your repository.
Meeting notes, Slack threads, and ticket exports often contain other people's names and
personal data — Bluewright treats that material as ordinary text and does not redact,
classify, or transmit it. Where it ends up is your repository's access model, not ours.
Worth remembering before you push a workspace somewhere public.

## Anthropic

Using Bluewright means using Claude Code, so your prompts and the files Claude reads go to
Anthropic as part of normal operation, governed by
[Anthropic's privacy policy](https://www.anthropic.com/legal/privacy). Bluewright adds
nothing to that flow and diverts nothing out of it.

## Questions

Email <valeriy.maslov.dev@gmail.com>. If you believe something here is inaccurate about
what the code actually does, that is a security report — see [`SECURITY.md`](SECURITY.md).

Changes to this document are tracked in [`CHANGELOG.md`](CHANGELOG.md) and in this
repository's history.
