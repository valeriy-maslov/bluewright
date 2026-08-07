# Security Policy

Bluewright is a Claude Code plugin: almost everything in it is a prompt that Claude reads
at runtime, plus one small Python hook. That shapes what a vulnerability looks like here —
see [Scope](#scope) before reporting.

## Supported versions

Only the latest release receives security fixes. Check yours with `/plugin list`, and see
[how a fix reaches you](#how-a-fix-reaches-you) below.

## Reporting a vulnerability

**Please do not open a public issue.**

- **Preferred** — [report privately through GitHub](https://github.com/valeriy-maslov/bluewright/security/advisories/new)
  (repository → **Security** → **Report a vulnerability**).
- **Alternative** — email <valeriy.maslov.dev@gmail.com> with `bluewright security` in the
  subject.

Helpful to include: the command you ran, the state of the workspace it ran in, the plugin
version and your Claude Code version (`claude --version`), and a transcript excerpt if you
have one.

> A Claude Code transcript can contain your own file contents, paths, and prompts. Redact
> before sending — a minimal reproduction is worth more than a full session log.

## What to expect

| Stage | Target |
|---|---|
| Acknowledgement | 5 business days |
| Initial assessment, with a severity call | 10 business days |
| Fix or mitigation for a confirmed high-severity issue | 30 days |
| Everything else | Best effort, tracked publicly once a fix ships |

Bluewright is maintained by one person. These targets are deliberately modest, and you will
get a straight answer if something slips.

## Scope

### In scope

- **The version hook** (`hooks/check-workspace-version.py`) doing anything beyond comparing
  two version strings: writing files, making network calls, recording prompt content, or
  executing anything it reads from `workspace.yml`. Also: any input that makes it crash in a
  way that blocks every prompt in a session.
- **Escaping a documented boundary.** Every agent is declared read-only and confined to the
  investigation folder (or, for `system-surveyor`, to one watched path). A component that
  writes when it shouldn't, or reads outside its stated boundary, is a bug worth reporting
  privately.
- **Path traversal.** The hook walks up the directory tree looking for `workspace.yml`, and
  commands write inside the investigation folder. Anything that escapes either — through
  symlinks, crafted paths, or otherwise — is in scope.
- **Privilege escalation through prompt injection.** Bluewright deliberately feeds untrusted
  material to Claude: files you drop in `inputs/`, repositories on your watchlist, web pages
  `option-scout` fetches. If such content can push an agent *past its declared tool list* —
  a read-only agent running shell commands, or any component exfiltrating file contents —
  that is a vulnerability.
- **Anything in this repository that executes at install time.** There is nothing today, and
  there should never be.

### Out of scope, by design

- **`/bluewright:spike` runs and installs things.** That is its entire purpose: it is the one
  sanctioned place for experiments, and every command still goes through Claude Code's own
  permission prompts. That it can execute code is not a vulnerability.
- **Prompt injection that only changes what a component says.** Untrusted input can skew a
  digest or bias a recommendation. That is a property of the medium, not a defect we can
  patch away; the mitigations are read-only tool lists and the fact that every artifact
  lands in a file you review. Escalation *past* the tool list is in scope — see above.
- **Claude Code itself** — its permission system, sandboxing, or model behaviour. Report
  those to Anthropic through [their process](https://www.anthropic.com/responsible-disclosure-policy).

### Known considerations

`/bluewright:publish` shells out to PlantUML (and Graphviz) to render `.puml` files.
PlantUML's `!include` directive can pull in local files and remote URLs, so rendering a
diagram you did not author carries the usual file-disclosure and SSRF exposure. Diagrams in
an investigation are normally written by you or by Claude inside that folder — but if you
ever render a `.puml` from an untrusted source, that is the risk you are taking, and it is
PlantUML's behaviour rather than something Bluewright can mediate.

## How a fix reaches you

`plugin.json` pins an explicit `version`, and Claude Code treats that string as the update
key. New commits alone do not reach installed users — the version has to change. A security
fix therefore ships as:

1. the fix, plus a version bump in `.claude-plugin/plugin.json`;
2. a `CHANGELOG.md` entry and a tagged GitHub release;
3. an updated commit pin in whichever marketplace you installed from.

Then update with `/plugin update bluewright@<marketplace>` — `bluewright@bluewright` if you
added this repository directly. Restart Claude Code or start a new session afterwards so the
hook reloads.

## Disclosure

Confirmed issues are published as a
[GitHub Security Advisory](https://github.com/valeriy-maslov/bluewright/security/advisories)
once a fix is available, and noted in the changelog. Reporters are credited by default —
tell us if you would rather not be. Please give us a chance to ship a fix before disclosing
publicly; if 90 days pass without one, go ahead.
