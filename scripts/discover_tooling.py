#!/usr/bin/env python3
"""Discover every skill, plugin, command and MCP server available to an agent.

    python3 scripts/discover_tooling.py                # write status/TOOLING.md + status/tooling.json
    python3 scripts/discover_tooling.py --check        # CI: the committed inventory is well-formed
    python3 scripts/discover_tooling.py --check-fresh  # local: the committed inventory matches this machine
    python3 scripts/discover_tooling.py --json         # print the inventory to stdout

The two checks are deliberately separate. `--check` is environment-agnostic and runs
in CI; `--check-fresh` compares against the machine you are on, which is the only
place where the answer is meaningful (a CI runner has no agent configuration).

The point is that an agent never has to guess what it has: global skills
(`${HOME}/.claude/skills`), plugins and marketplaces, project skills
(`.claude/skills`), slash commands, and MCP servers from every configuration
level are collected into one report.

Secrets: MCP environment variables are reported by NAME only, never by value.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
HOME = Path.home()
OUT_MD = ROOT / "status" / "TOOLING.md"
OUT_JSON = ROOT / "status" / "tooling.json"

# Skill names that matter for this project, matched case-insensitively.
DOMAIN_HINTS = {
    "android": ["android", "compose", "kotlin", "wear", "leanback", "mobile", "play-", "r8", "camerax", "media3"],
    "ui-design": ["design", "ui", "ux", "craft", "polish", "typeset", "color", "layout", "typography", "font"],
    "process": ["plan", "autoresearch", "karpathy", "orchestrator", "task", "priority", "effort", "review", "audit"],
    "security": ["security", "intent", "policy", "credential", "governors"],
    "backend": ["api", "server", "database", "auth", "migration", "testing", "verify"],
    "media": ["image", "video", "higgsfield", "audio", "speech", "brand"],
}


def run(cmd: list[str]) -> str | None:
    try:
        out = subprocess.run(cmd, capture_output=True, text=True, timeout=20, check=False)
    except (OSError, subprocess.SubprocessError):
        return None
    return out.stdout.strip() if out.returncode == 0 else None


def list_skill_dirs(base: Path) -> list[str]:
    if not base.is_dir():
        return []
    names = []
    for entry in sorted(base.iterdir()):
        if entry.is_dir() and (entry / "SKILL.md").exists():
            names.append(entry.name)
        elif entry.is_file() and entry.suffix == ".md":
            names.append(entry.stem)
    return names


def categorise(skills: list[str]) -> dict[str, list[str]]:
    groups: dict[str, list[str]] = {k: [] for k in DOMAIN_HINTS}
    groups["other"] = []
    for name in skills:
        low = name.lower()
        placed = False
        for group, hints in DOMAIN_HINTS.items():
            if any(h in low for h in hints):
                groups[group].append(name)
                placed = True
                break
        if not placed:
            groups["other"].append(name)
    return {k: v for k, v in groups.items() if v}


def read_json(path: Path):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None


def mcp_from_claude_json() -> dict[str, list[dict]]:
    """MCP servers from ~/.claude.json: global plus per-project entries."""
    data = read_json(HOME / ".claude.json") or {}
    found: dict[str, list[dict]] = {}

    def collect(servers, scope: str):
        if not isinstance(servers, dict):
            return
        for name, cfg in servers.items():
            cfg = cfg if isinstance(cfg, dict) else {}
            entry = {
                "name": name,
                "scope": scope,
                "transport": cfg.get("type") or ("stdio" if cfg.get("command") else cfg.get("url") and "http"),
                "env_keys": sorted((cfg.get("env") or {}).keys()),
                "has_args": bool(cfg.get("args")),
                "url_host": (cfg.get("url") or "").split("/")[2] if cfg.get("url") else None,
            }
            found.setdefault(name, []).append(entry)

    collect(data.get("mcpServers"), "user")
    for project_path, project in (data.get("projects") or {}).items():
        if isinstance(project, dict):
            collect(project.get("mcpServers"), f"project:{project_path}")
    return found


def mcp_from_project_files() -> dict[str, list[dict]]:
    """MCP servers declared inside this repository (project scope)."""
    found: dict[str, list[dict]] = {}
    candidates = [
        ROOT / ".mcp.json",
        ROOT / ".cursor" / "mcp.json",
        ROOT / ".claude" / "settings.json",
        ROOT / ".vscode" / "mcp.json",
    ]
    for path in candidates:
        data = read_json(path)
        if not isinstance(data, dict):
            continue
        servers = data.get("mcpServers") or {}
        for name, cfg in (servers.items() if isinstance(servers, dict) else []):
            cfg = cfg if isinstance(cfg, dict) else {}
            found.setdefault(name, []).append(
                {
                    "name": name,
                    "scope": f"file:{path.relative_to(ROOT)}",
                    "transport": cfg.get("type") or ("stdio" if cfg.get("command") else "http"),
                    "env_keys": sorted((cfg.get("env") or {}).keys()),
                }
            )
    return found


def collect() -> dict:
    global_skills_dir = HOME / ".claude" / "skills"
    project_skills_dir = ROOT / ".claude" / "skills"
    global_skills = list_skill_dirs(global_skills_dir)
    project_skills = list_skill_dirs(project_skills_dir)

    plugins_installed = read_json(HOME / ".claude" / "plugins" / "installed_plugins.json") or {}
    plugins = []
    for key, installs in (plugins_installed.get("plugins") or {}).items():
        versions = [i.get("version") for i in installs if isinstance(i, dict)]
        plugins.append({"name": key, "scopes": sorted({i.get("scope") for i in installs if isinstance(i, dict)}), "versions": versions})

    marketplaces = read_json(HOME / ".claude" / "plugins" / "known_marketplaces.json") or {}

    legacy_inventory = read_json(HOME / ".claude" / "global-toolchain-inventory.json") or {}

    design_library = HOME / ".claude" / "design-skill-library"
    design_entries = 0
    curation = design_library / "CURATION.tsv"
    if curation.exists():
        try:
            design_entries = sum(1 for _ in curation.open(encoding="utf-8")) - 1
        except OSError:
            design_entries = 0

    mcp = mcp_from_claude_json()
    for name, entries in mcp_from_project_files().items():
        mcp.setdefault(name, []).extend(entries)

    skills_cli = run(["npx", "--no-install", "skills", "--help"]) is not None

    return {
        "environment": {
            "platform": sys.platform,
            "machine": os.uname().machine if hasattr(os, "uname") else "unknown",
            "home": str(HOME),
            "project": str(ROOT),
        },
        "global_skills_dir": str(global_skills_dir),
        "global_skills": global_skills,
        "global_skills_by_domain": categorise(global_skills),
        "project_skills_dir": str(project_skills_dir),
        "project_skills": project_skills,
        "plugins": plugins,
        "marketplaces": sorted(marketplaces.keys()),
        "slash_commands": sorted(p.stem for p in (HOME / ".claude" / "commands").glob("*.md")) if (HOME / ".claude" / "commands").is_dir() else [],
        "design_library": {
            "path": str(design_library),
            "entries": design_entries,
            "index": (design_library / "INDEX.md").exists(),
        },
        "skills_cli": skills_cli,
        "mcp_servers": mcp,
        "legacy_inventory_present": bool(legacy_inventory),
        "claude_agents_global_dir": (HOME / ".claude" / "agents").is_dir(),
    }


def render_md(inv: dict) -> str:
    g = inv["global_skills"]
    p = inv["project_skills"]
    lines: list[str] = []
    add = lines.append

    add("# Tooling Inventory")
    add("")
    add("Generated by [`scripts/discover_tooling.py`](../scripts/discover_tooling.py) — do not edit by hand.")
    add("Regenerate with `python3 scripts/discover_tooling.py`. CI validates its structure (`--check`);")
    add("the freshness check (`--check-fresh`) is meaningful only on a machine that has agent configuration.")
    add("")
    add("**Agents: read this before starting a task.** It is the list of skills, plugins and MCP servers")
    add("available to you. Using an installed skill beats writing the equivalent instruction by hand.")
    add("Rules and precedence: [handbooks/08-tooling-discovery.md](../handbooks/08-tooling-discovery.md).")
    add("")

    add("## Summary")
    add("")
    add("| Source | Count |")
    add("|---|---|")
    add(f"| Global skills (`~/.claude/skills`) | {len(g)} |")
    add(f"| Project skills (`.claude/skills`) | {len(p)} |")
    add(f"| Plugins installed | {len(inv['plugins'])} |")
    add(f"| Marketplaces known | {len(inv['marketplaces'])} |")
    add(f"| Slash commands | {len(inv['slash_commands'])} |")
    add(f"| MCP servers discovered | {len(inv['mcp_servers'])} |")
    add(f"| Design skill library entries | {inv['design_library']['entries']} |")
    add(f"| `npx skills` available | {'yes' if inv['skills_cli'] else 'no'} |")
    add("")

    add("## Project skills (authoritative for this repository)")
    add("")
    if p:
        for name in p:
            add(f"- `{name}`")
    else:
        add("- none found — create one under `.claude/skills/<name>/SKILL.md`")
    add("")

    add("## Global skills by domain")
    add("")
    for group, names in inv["global_skills_by_domain"].items():
        add(f"**{group}** ({len(names)}): " + ", ".join(f"`{n}`" for n in names))
        add("")

    add("## Plugins")
    add("")
    if inv["plugins"]:
        add("| Plugin | Scope | Version |")
        add("|---|---|---|")
        for plugin in inv["plugins"]:
            add(f"| `{plugin['name']}` | {', '.join(plugin['scopes'])} | {', '.join(plugin['versions'])} |")
    else:
        add("- none installed (plugins add skills and subagents; install with the plugin marketplace commands)")
    add("")
    add(f"Known marketplaces: {', '.join('`' + m + '`' for m in inv['marketplaces']) or 'none'}")
    add("")
    add(f"Slash commands: {', '.join('`/' + c + '`' for c in inv['slash_commands']) or 'none'}")
    add("")
    add(
        "Design library: "
        f"{inv['design_library']['entries']} curated entries at `{inv['design_library']['path']}`"
        + (" (index present)" if inv["design_library"]["index"] else "")
    )
    add("")

    add("## MCP servers")
    add("")
    if inv["mcp_servers"]:
        add("| Server | Scope | Transport | Env keys (names only) |")
        add("|---|---|---|---|")
        for name, entries in sorted(inv["mcp_servers"].items()):
            for entry in entries:
                env = ", ".join(f"`{k}`" for k in entry.get("env_keys") or []) or "—"
                add(f"| `{name}` | {entry['scope']} | {entry.get('transport') or 'unknown'} | {env} |")
        add("")
        add("Environment **values** are deliberately never recorded here — only their names.")
    else:
        add("- No MCP servers are configured in any discovered scope yet.")
        add("- To add one for this repository, copy [`.mcp.json.example`](../.mcp.json.example) to `.mcp.json`")
        add("  and fill in the server definition; Claude Code picks it up on the next session.")
        add("- DroidRoute itself federates MCP servers at runtime (`docs/07-mcp-plugins.md`).")
    add("")

    add("## How to use this inventory")
    add("")
    add("1. Pick the skill that matches the workstream, not the one with the nicest name.")
    add("2. Prefer a project skill for project rules, a global skill for technique.")
    add("3. Use at least two skills per task in parallel (implementation + verification).")
    add("4. If nothing fits, search for one before writing your own: `npx skills find <query>`.")
    add("5. Record substitutions in the task log: `skill-substitution: <old> -> <new> (<reason>)`.")
    add("")

    add("## Regenerating")
    add("")
    add("```bash")
    add("python3 scripts/discover_tooling.py                # refresh status/TOOLING.md and status/tooling.json")
    add("python3 scripts/discover_tooling.py --check        # validate structure (CI)")
    add("python3 scripts/discover_tooling.py --check-fresh  # validate against this machine")
    add("```")
    add("")
    return "\n".join(lines)


def fingerprint(inv: dict) -> str:
    return hashlib.sha256(json.dumps(inv, sort_keys=True).encode("utf-8")).hexdigest()[:16]


REQUIRED_JSON_KEYS = (
    "environment",
    "global_skills",
    "project_skills",
    "plugins",
    "marketplaces",
    "slash_commands",
    "design_library",
    "skills_cli",
    "mcp_servers",
)

REQUIRED_MD_SECTIONS = (
    "# Tooling Inventory",
    "## Summary",
    "## Project skills",
    "## Global skills by domain",
    "## Plugins",
    "## MCP servers",
    "## How to use this inventory",
    "## Regenerating",
)


def check_structure() -> int:
    """Environment-agnostic validation: the committed inventory is well formed.

    This is what CI runs. A CI runner has no `~/.claude`, so comparing content
    there would fail for the wrong reason.
    """
    problems: list[str] = []

    if not OUT_JSON.exists():
        problems.append("status/tooling.json is missing")
    else:
        try:
            data = json.loads(OUT_JSON.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            problems.append(f"status/tooling.json is not valid JSON: {exc}")
            data = None
        if isinstance(data, dict):
            for key in REQUIRED_JSON_KEYS:
                if key not in data:
                    problems.append(f"status/tooling.json is missing key '{key}'")
            for key in ("global_skills", "project_skills", "plugins", "marketplaces", "slash_commands"):
                if key in data and not isinstance(data[key], list):
                    problems.append(f"status/tooling.json: '{key}' must be a list")
            if "mcp_servers" in data and not isinstance(data["mcp_servers"], dict):
                problems.append("status/tooling.json: 'mcp_servers' must be an object")

    if not OUT_MD.exists():
        problems.append("status/TOOLING.md is missing")
    else:
        text = OUT_MD.read_text(encoding="utf-8")
        for section in REQUIRED_MD_SECTIONS:
            if section not in text:
                problems.append(f"status/TOOLING.md is missing the section '{section}'")
        if "Environment **values**" not in text and "No MCP servers" not in text:
            problems.append("status/TOOLING.md does not state the MCP secret policy")

    if problems:
        print("tooling inventory is malformed:", file=sys.stderr)
        for problem in problems:
            print(f"  - {problem}", file=sys.stderr)
        print("fix: python3 scripts/discover_tooling.py", file=sys.stderr)
        return 1

    print("tooling inventory is well formed (structure check)")
    return 0


def check_freshness(environment_inventory: dict, markdown: str) -> int:
    """Compare the committed inventory with this machine.

    Only meaningful where agent configuration exists; a bare container reports
    'nothing to compare' instead of failing a build for the wrong reason.
    """
    if not environment_inventory["global_skills"] and not environment_inventory["plugins"]:
        print("no agent configuration on this machine — freshness cannot be judged here (structure check only)")
        return check_structure()

    current = OUT_MD.read_text(encoding="utf-8") if OUT_MD.exists() else ""
    if current != markdown:
        print("tooling inventory is stale — run: python3 scripts/discover_tooling.py", file=sys.stderr)
        return 1

    print(
        f"tooling inventory current "
        f"({len(environment_inventory['global_skills'])} global skills, "
        f"{len(environment_inventory['project_skills'])} project skills, "
        f"{len(environment_inventory['mcp_servers'])} MCP servers)"
    )
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="validate the committed inventory is well formed (CI)")
    parser.add_argument(
        "--check-fresh",
        action="store_true",
        dest="check_fresh",
        help="validate the committed inventory matches this machine (local)",
    )
    parser.add_argument("--json", action="store_true", help="print to stdout instead of writing")
    args = parser.parse_args()

    inventory = collect()
    inventory["fingerprint"] = fingerprint(inventory)
    markdown = render_md(inventory)

    if args.json:
        print(json.dumps(inventory, indent=2))
        return 0

    if args.check:
        return check_structure()

    if args.check_fresh:
        return check_freshness(inventory, markdown)

    OUT_MD.parent.mkdir(parents=True, exist_ok=True)
    OUT_MD.write_text(markdown, encoding="utf-8")
    OUT_JSON.write_text(json.dumps(inventory, indent=2) + "\n", encoding="utf-8")
    print(
        f"wrote {OUT_MD.relative_to(ROOT)} — "
        f"{len(inventory['global_skills'])} global skills, {len(inventory['project_skills'])} project skills, "
        f"{len(inventory['plugins'])} plugins, {len(inventory['mcp_servers'])} MCP servers"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
