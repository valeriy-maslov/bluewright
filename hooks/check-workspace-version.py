#!/usr/bin/env python3
"""UserPromptSubmit hook: enforce plugin/workspace version compatibility.

Fires on every prompt; does nothing unless the prompt invokes a
/bluewright:* command. Two commands are exempt: /bluewright:init, which
creates workspaces and has nothing to compare against, and
/bluewright:migrate, which is the remedy for the blocks below and must stay
reachable in exactly the workspaces they stop.

Rules (see docs/spec.md, "Versioning"):
  - workspace newer than plugin          -> BLOCK (exit 2): update the plugin
  - workspace older, different MAJOR     -> BLOCK (exit 2): run /bluewright:migrate
  - workspace older, same major          -> allow, add a context note (stdout)
  - bluewright field missing             -> allow, add a context note (stdout)
  - equal versions / not in a workspace  -> allow, silent
  - /bluewright:init, /bluewright:migrate -> allow, silent, always
"""

import json
import os
import re
import sys

COMMAND_RE = re.compile(r"^\s*/bluewright:(?P<cmd>[a-z-]+)\b")
EXEMPT_COMMANDS = frozenset({"init", "migrate"})
VERSION_RE = re.compile(r"^bluewright:\s*[\"']?(\d+\.\d+\.\d+)[\"']?\s*$")


def parse_version(text):
    m = re.match(r"^(\d+)\.(\d+)\.(\d+)$", text.strip())
    return tuple(int(p) for p in m.groups()) if m else None


def find_workspace(start):
    d = os.path.realpath(start)
    while True:
        marker = os.path.join(d, "workspace.yml")
        if os.path.isfile(marker):
            return marker
        parent = os.path.dirname(d)
        if parent == d:
            return None
        d = parent


def workspace_version(marker_path):
    with open(marker_path, encoding="utf-8") as f:
        for line in f:
            m = VERSION_RE.match(line)
            if m:
                return parse_version(m.group(1))
    return None


def plugin_version():
    plugin_root = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
    manifest = os.path.join(plugin_root, ".claude-plugin", "plugin.json")
    with open(manifest, encoding="utf-8") as f:
        return parse_version(json.load(f)["version"])


def main():
    try:
        payload = json.load(sys.stdin)
    except (json.JSONDecodeError, ValueError):
        return 0  # malformed input: never break the prompt over the hook itself

    m = COMMAND_RE.match(payload.get("prompt", ""))
    if not m or m.group("cmd") in EXEMPT_COMMANDS:
        return 0

    marker = find_workspace(payload.get("cwd") or os.getcwd())
    if marker is None:
        return 0  # not in a workspace: the command reports this itself

    ws = workspace_version(marker)
    plug = plugin_version()
    if plug is None:
        return 0  # unreadable manifest: don't block on our own bug

    if ws is None:
        print(
            f"Note: {marker} has no 'bluewright' field. Add "
            f'\'bluewright: "{".".join(map(str, plug))}"\' to record the '
            "workspace format version (see the bluewright spec, Versioning)."
        )
        return 0

    if ws == plug:
        return 0

    ws_s = ".".join(map(str, ws))
    plug_s = ".".join(map(str, plug))

    if ws > plug:
        print(
            f"Bluewright: this workspace was created with plugin v{ws_s}, "
            f"but v{plug_s} is installed. Update the plugin first "
            "(/plugin update bluewright@bluewright), then retry.",
            file=sys.stderr,
        )
        return 2

    if ws[0] != plug[0]:
        print(
            f"Bluewright: this workspace uses format v{ws_s}; installed "
            f"plugin v{plug_s} has a breaking format change. Run "
            "/bluewright:migrate to bring the workspace up to date, then "
            "retry.",
            file=sys.stderr,
        )
        return 2

    print(
        f"Note: this Bluewright workspace was created with plugin v{ws_s}; "
        f"v{plug_s} is installed (compatible). /bluewright:migrate can update "
        "the recorded version."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
