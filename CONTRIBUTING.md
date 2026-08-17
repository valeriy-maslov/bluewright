# Contributing to Bluewright

Thanks for taking an interest. Bluewright is a Claude Code plugin, which means almost
everything in this repository is a **prompt**, not a program — Markdown files with YAML
frontmatter that Claude reads at runtime. Contributing is mostly careful writing, and the
review bar is about behaviour: does the command still do the right thing, on a real
workspace, without stepping outside its boundary?

## Before you start

- **Bugs and rough edges** — open an issue with the command you ran, what you expected,
  and what happened. Paste the relevant transcript if you can; prompts fail in ways stack
  traces don't capture.
- **New commands, agents, or skills** — open an issue first. Bluewright deliberately has a
  small surface, and a new `/bluewright:*` command is a commitment. Describe the workflow
  gap before writing the prompt.
- **Fixes to wording, examples, or docs** — just send the pull request.
- **Security problems** — not in an issue, please. Follow [`SECURITY.md`](SECURITY.md).
- **Anything that collects, stores, or transmits data** — it won't be merged. See
  [`PRIVACY.md`](PRIVACY.md) for the promises a change has to keep.

## Local development

Install the plugin from your checkout rather than from GitHub:

```
/plugin marketplace add /path/to/bluewright
/plugin install bluewright@bluewright
```

Reinstalling is version-gated: bump `version` in `.claude-plugin/plugin.json` before
`/plugin update bluewright@bluewright` will pick your changes up. Restart Claude Code (or
start a new session) after installing so commands, agents, skills, and the hook load.

## Where things go

| Path | Holds | Notes |
|---|---|---|
| `commands/` | The `/bluewright:*` slash commands | One file per command; the filename is the command name. |
| `agents/` | Read-only subagents the commands dispatch | Never write files, never touch the network. |
| `skills/<name>/SKILL.md` | Reusable procedures shared by commands | Format details belong in the spec, procedure and quality bar belong here. |
| `hooks/` | `check-workspace-version.py` and its registration | The only executable code shipped to users. |
| `.github/workflows/` | `validate.yml` (manifest checks) and `release.yml` (changelog-driven releases) | CI only; not part of the installed plugin. |
| `docs/spec.md` | The on-disk contract | Single source of truth for layout, file formats, and IDs. |
| `docs/manual.html` | The user manual | Keep in sync when user-visible behaviour changes. |

## Conventions

**The spec wins.** `docs/spec.md` defines the workspace layout, file formats, ID schemes,
and resolution rules. Commands and skills describe *procedure* and reference the spec for
*format* — they don't restate it. If a change needs a different file shape, change the
spec in the same pull request and say so explicitly.

**Frontmatter.** Commands carry `description`, `argument-hint` (when they take one), and
`allowed-tools`. Agents carry `name`, `description`, and `tools`. Skills carry `name` and
`description`. The `description` is what Claude uses to decide when to reach for the
thing, so write it for that job: say what it does, when it's dispatched, and what it
returns.

**Least privilege.** Give a command or agent only the tools it actually needs. Read-only
commands (`/bluewright:status`, `/bluewright:ask`) must stay read-only. Agents get `Bash`
for inspection only — `git log`, `ls`, `grep`, scoped to their target. No command installs
or runs arbitrary code; `/bluewright:make-artifact` shelling out to a deterministic local
PlantUML renderer is the one exception, and it stays that narrow.

**Stay inside the workspace.** Per the spec's boundary rule, commands read and write only
within the workspace tree, with two exceptions: watchlist paths the user configured, and
the target path given to `/bluewright:init`. New prompts must not introduce global state,
home-directory config, or a registry.

**Plugin-relative paths.** Reference files shipped with the plugin through
`${CLAUDE_PLUGIN_ROOT}` (for example `${CLAUDE_PLUGIN_ROOT}/docs/spec.md`), never a
hard-coded or relative path.

**Prose style.** Match what's already there — direct, second person, concrete. Prefer a
numbered `## Steps` section over a wall of narrative, and say what the command must *not*
do as plainly as what it must.

## Checks before you open a pull request

There is no automated test suite; validation is a manifest check plus a real run.

1. **Validate the manifests:**

   ```bash
   claude plugin validate .claude-plugin/marketplace.json --strict
   claude plugin validate .claude-plugin/plugin.json --strict
   ```

   Both paths are needed. `claude plugin validate .` resolves to the marketplace manifest
   only and silently skips everything else. Pointing at `plugin.json` is what walks
   `agents/`, `commands/`, `skills/`, and `hooks/hooks.json`.

   `--strict` turns warnings — unknown manifest fields, missing frontmatter descriptions —
   into a non-zero exit. CI runs exactly these two commands on every push and pull request
   (`.github/workflows/validate.yml`), so a warning you ignore locally fails the build.

2. **Exercise the hook** if you touched `hooks/`:

   ```bash
   echo '{"prompt":"/bluewright:status","cwd":"/path/to/a/workspace"}' \
     | ./hooks/check-workspace-version.py; echo "exit=$?"
   ```

   Exit `0` allows the prompt, exit `2` blocks it with the stderr message. Cover the cases
   listed in the module docstring: workspace newer than the plugin, a major-version gap, a
   compatible older workspace, a missing `bluewright` field, and not being in a workspace
   at all. The hook must never break a prompt because of its own failure — malformed input
   and unreadable manifests exit `0`.

   One case is load-bearing and easy to break: **`/bluewright:migrate` must exit `0` in a
   workspace with a major-version gap**, where everything else exits `2`. It is the remedy
   for that block, so blocking it locks the user out with no way forward.

   ```bash
   echo '{"prompt":"/bluewright:migrate","cwd":"/path/to/an/old/workspace"}' \
     | ./hooks/check-workspace-version.py; echo "exit=$?"   # must be 0
   ```

3. **Smoke-test the change against a scratch workspace:**

   ```
   /bluewright:init ~/tmp/bw-test
   /bluewright:new sample-feature
   ```

   Then run the command you changed and read what it wrote. Prompts regress silently —
   inspecting the resulting files is the test.

4. **Update the docs** — `README.md` for a new or renamed command, `docs/manual.html` for
   user-visible behaviour, `docs/spec.md` for anything on disk.

## Versioning

Bluewright follows [semantic versioning](https://semver.org/) on
`.claude-plugin/plugin.json`, and workspaces record the version that created them:

| Change | Bump |
|---|---|
| Wording, prompt tuning, bug fix — no change to what's written on disk | patch |
| New command, agent, or skill; new optional file or field | minor |
| Breaking change to the workspace format — anything a v1 workspace can't be read as | major |

The major bump matters: `hooks/check-workspace-version.py` blocks commands when the
workspace and plugin majors differ, telling the user migration is required. Don't reshape
an existing file format without one.

Every user-visible change gets a line in [`CHANGELOG.md`](CHANGELOG.md) under
`## [Unreleased]`, grouped as Added / Changed / Fixed / Removed. Write it for someone
deciding whether to update — what they can now do, or what behaves differently — and say
so explicitly when the change touches what's written on disk.

## Releasing

The changelog is the release trigger. To cut a version:

1. Rename `## [Unreleased]` to `## [X.Y.Z] — YYYY-MM-DD`, add a fresh empty
   `## [Unreleased]` above it, and update the link definitions at the bottom of the file.
2. Set the same `X.Y.Z` in `.claude-plugin/plugin.json`.
3. Merge to `master`.

`.github/workflows/release.yml` takes it from there: on any push to `master` that touches
`CHANGELOG.md`, it reads the topmost released section, tags the commit `vX.Y.Z`, and
publishes a GitHub release with that section as the notes.

Three things about it are worth knowing:

- **The version must match.** If the top of the changelog and `plugin.json` disagree, the
  job fails rather than releasing the wrong number. Bump both in the same commit.
- **It's idempotent.** A version that's already released is skipped, so editing a typo in
  a shipped entry — or adding a line under `Unreleased` — publishes nothing.
- **It can be re-run by hand.** Use the workflow's `Run workflow` button
  (`workflow_dispatch`) if a run failed for an unrelated reason.

A version with a pre-release identifier (`1.1.0-rc.1`) is published as a GitHub
pre-release automatically.

## Pull requests

- Branch off `master` and keep the pull request focused on one change.
- Write commit subjects in the imperative mood (`add promote command`, not `added…`),
  under ~72 characters, with the reasoning in the body when it isn't obvious.
- In the description, say what you ran to check it — the validate output and which command
  you exercised on a scratch workspace.
- Bump the plugin version in the same pull request when the change warrants one, per the
  table above, and add the changelog entry alongside it.

Contributions are accepted under the repository's [MIT license](LICENSE).
