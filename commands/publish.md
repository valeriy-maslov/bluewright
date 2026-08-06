---
description: Make outputs/ shareable — render .puml diagrams to .png, verify self-containment, refresh the index, report staleness
argument-hint: [feature-slug, optional inside a workspace]
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, Task
---

Prepare an investigation's `outputs/` folder for **sharing**: everything
rendered, nothing pointing outside the folder, staleness stated instead of
hidden. `outputs/` is the only thing colleagues ever receive — after this
command it must survive being zipped and mailed.

First read the spec at `${CLAUDE_PLUGIN_ROOT}/docs/spec.md` and follow its
formats and resolution rules exactly.

Argument: `$ARGUMENTS`

## Steps

1. **Resolve** the workspace and investigation per the spec. Empty
   `outputs/` → nothing to publish; point at `/bluewright:brief` and stop.
2. **Detect the renderer**: local `plantuml` CLI, else docker one-shot
   (`docker run --rm plantuml/plantuml`), else none — diagrams will be
   reported unrendered, not silently skipped.
3. **Dispatch one `bluewright:doc-builder`** (Task) with the investigation
   path and the detected renderer. It renders and verifies; it does not fix.
4. **Fix what the digest reports**, in the open:
   - escaping links → repoint to the in-`outputs/` artifact, or copy the
     referenced input into `outputs/` if it genuinely must ship;
   - dangling ID references → correct the typo'd ID, or flag it if the
     referenced entry truly doesn't exist (that's a content bug, not a
     link bug);
   - render failures → fix trivial `.puml` syntax errors and re-render;
     anything deeper gets reported, not buried.
   Never alter meaning while fixing — wording and claims belong to the
   commands that wrote them.
5. **Refresh `outputs/README.md`**: title, phase, generated date, then the
   inventory — each artifact with its one-line purpose, stale ones marked
   `⚠ stale: <reason>`. The README is the reading order for a stranger.
6. **Report** one screen: what is now shareable, diagrams rendered/failed,
   fixes applied, and the honest staleness list with the command that would
   refresh each stale artifact (`/brief`, `/options`, `/design`).

## Rules

- Publishing never regenerates content: a stale brief is marked stale, not
  rewritten here — that's `/brief`'s job. This command ships the truth,
  including the inconvenient parts.
- No standing services: rendering is one-shot, local or docker.
- Everything outside `outputs/` is read-only to this command.
