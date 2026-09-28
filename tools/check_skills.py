#!/usr/bin/env python3
"""Check that every role label in the plan resolves to something installed.

    python3 tools/check_skills.py

Three questions, three failure modes:

1. Does every label used in ``tools/plan_data/`` have a row in
   ``handbooks/09-skill-resolution.md``?  (A missing row means the agent has no
   idea which tool to load and will improvise.)
2. Does every ``skill:`` / ``plugin:`` / ``mcp:`` token in that page exist in
   ``status/tooling.json``?  (A token for a library that is not installed is a
   silent no-op, which is worse than an error.)
3. Does the table still earn its space — are there rows no task uses?

Exit code 0 when the mapping is complete and installed, 1 otherwise.
Rows that no task uses are reported as warnings only: a label may be added
ahead of the task that needs it.
"""

from __future__ import annotations

import importlib.util
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "tools" / "plan_data"
RESOLUTION = ROOT / "handbooks" / "09-skill-resolution.md"
INVENTORY = ROOT / "status" / "tooling.json"

TOKEN = re.compile(r"\b(skill|plugin|mcp):([a-z0-9][a-z0-9._-]*)")
ROW = re.compile(r"^\|\s*`([a-z0-9][a-z0-9-]*)`\s*\|(.+)\|\s*$")


def load_plan_labels() -> dict[str, int]:
    """Role labels used by the plan, with the number of tasks using each."""
    sys.path.insert(0, str(DATA_DIR))
    labels: dict[str, int] = {}
    for path in sorted(DATA_DIR.glob("phase_*.py")):
        spec = importlib.util.spec_from_file_location(path.stem, path)
        if spec is None or spec.loader is None:  # pragma: no cover
            raise RuntimeError(f"cannot load {path}")
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        for task in module.TASKS:
            for name, _role in task.skills:
                labels[name] = labels.get(name, 0) + 1
    return labels


def load_installed() -> tuple[set[str], set[str], set[str]]:
    """(skills, plugins, mcp servers) actually present on this machine."""
    data = json.loads(INVENTORY.read_text(encoding="utf-8"))
    skills = set(data.get("global_skills", [])) | set(data.get("project_skills", []))
    plugins = {entry["name"].split("@", 1)[0] for entry in data.get("plugins", [])}
    servers: set[str] = set()
    for entry in data.get("mcp_servers", []):
        if isinstance(entry, str):
            servers.add(entry)
        elif isinstance(entry, dict) and "name" in entry:
            servers.add(entry["name"])
    return skills, plugins, servers


def main() -> int:
    for path in (RESOLUTION, INVENTORY):
        if not path.exists():
            print(f"missing {path.relative_to(ROOT)} — run the scaffolding first")
            return 1

    text = RESOLUTION.read_text(encoding="utf-8")
    used = load_plan_labels()
    skills, plugins, servers = load_installed()

    rows: dict[str, str] = {}
    for line in text.splitlines():
        match = ROW.match(line)
        if match:
            rows.setdefault(match.group(1), match.group(2))

    problems: list[str] = []

    # 1 — every plan label has a row
    for label in sorted(used):
        if label not in rows:
            problems.append(f"label `{label}` is used by {used[label]} task(s) but has no row in {RESOLUTION.name}")

    # 2 — every token resolves to something installed
    seen: set[tuple[str, str]] = set()
    for kind, name in TOKEN.findall(text):
        if (kind, name) in seen:
            continue
        seen.add((kind, name))
        if kind == "skill" and name not in skills:
            problems.append(f"skill:`{name}` is referenced but not installed (see status/TOOLING.md)")
        elif kind == "plugin" and name not in plugins:
            problems.append(f"plugin:`{name}` is referenced but not installed")
        elif kind == "mcp" and name not in servers:
            problems.append(f"mcp:`{name}` is referenced but not configured (inventory lists {len(servers)})")

    unused = sorted(set(rows) - set(used))

    for line in problems:
        print(f"FAIL  {line}")
    for label in unused:
        print(f"WARN  row `{label}` is not used by any task")

    if problems:
        print(f"\n{len(problems)} problem(s) in the skill resolution")
        return 1

    print(
        f"skill resolution ok — {len(used)} labels used, {len(rows)} rows, "
        f"{len(seen)} tool tokens all installed"
        + (f", {len(unused)} unused row(s)" if unused else "")
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
