#!/usr/bin/env python3
"""Consistency audit across the plan data, the generated tree and the documents.

    python3 tools/check_plan_consistency.py
    python3 tools/check_plan_consistency.py --quiet

This is the debugger for the build plan itself. It composes the other checkers
(plan freshness, links, skill labels, design gate) instead of re-implementing
them, and adds the invariants nothing else covers:

1. Task ids are unique, strictly increasing, and every dependency exists and points backwards.
2. Slugs and filenames are unique and safe.
3. No task is empty: goal, ≥2 skills, deliverables, ≥2 steps, ≥2 acceptance criteria, ≥1 verification command, and a stated end state.
4. Every ``T-0xx`` referenced in a document exists; a task nobody references is reported.
5. Every stated task count in the documents matches the real count — the drift that survived a phase addition before.
6. The kick-off file exists and its code word is reachable from the README.

Exit 0 when the plan is internally consistent, 1 otherwise.
"""

from __future__ import annotations

import argparse
import importlib.util
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "tools" / "plan_data"

TASK_REF = re.compile(r"\bT-(\d{3})\b")

# Only shapes that unambiguously state the size of the whole plan are checked.
# A bare "N tasks" is too ambiguous — it also appears in per-phase and log-count
# sentences, and a check that cries wolf gets disabled instead of fixed.
COUNT_CLAIMS = (
    re.compile(r"(?<![≥>\d])(?<!at least )(\d{2,3})\s+task files"),
    re.compile(r"(?<!\d)(\d{2,3})\s+[Tt]asks? in\s+(\d{1,2})\s+[Pp]hases?\b"),
    re.compile(r"all\s+(\d{2,3})\s+tasks\b"),
    re.compile(r"[Tt]asks complete:\s*\d+\s*/\s*(\d{2,3})"),
)
EST = re.compile(r"^\d+\s*-\s*\d+\s*min$")
SLUG = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")

DOC_DIRS = ("docs", "handbooks", "status")
DOC_FILES = ("README.md", "AGENTS.md", "CLAUDE.md", "CHANGELOG.md", "KICKOFF.md")
SKIP_DOCS = {"docs/droidroute-spec.md"}  # the owner's original spec: historical, not maintained


def load_phases():
    sys.path.insert(0, str(DATA_DIR))
    phases = []
    for path in sorted(DATA_DIR.glob("phase_*.py")):
        spec = importlib.util.spec_from_file_location(path.stem, path)
        if spec is None or spec.loader is None:  # pragma: no cover
            raise RuntimeError(f"cannot load {path}")
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        phases.append((module.PHASE, list(module.TASKS)))
    return phases


def run(command: list[str]) -> bool:
    result = subprocess.run(command, cwd=ROOT, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"  {command[1]} reported a problem:")
        for line in (result.stdout + result.stderr).strip().splitlines():
            print(f"    {line}")
    return result.returncode == 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--quiet", action="store_true", help="only print problems")
    args = parser.parse_args()

    phases = load_phases()
    problems: list[str] = []
    warnings: list[str] = []

    tasks: dict[int, object] = {}
    slugs: dict[str, int] = {}
    phase_of: dict[int, int] = {}
    order: list[int] = []

    # 1–3 — the plan data itself
    previous = 0
    for index, (phase, phase_tasks) in enumerate(phases):
        if phase.number != index:
            problems.append(f"phase {phase.number:02d} is at position {index} — phases must be contiguous from 00")
        if not phase_tasks:
            problems.append(f"phase {phase.number:02d} has no tasks")
        if phase.number in (7, 14) and not phase.design:
            problems.append(f"phase {phase.number:02d} has a visual surface but no design contract")
        for task in phase_tasks:
            ident = task.id
            if ident in tasks:
                problems.append(f"T-{ident:03d} is defined twice")
            if ident <= previous:
                problems.append(f"T-{ident:03d} does not increase (previous was T-{previous:03d})")
            previous = ident
            tasks[ident] = task
            phase_of[ident] = phase.number
            order.append(ident)

            if task.slug in slugs:
                problems.append(f"slug {task.slug!r} is used by T-{slugs[task.slug]:03d} and T-{ident:03d}")
            slugs[task.slug] = ident
            if not SLUG.match(task.slug):
                problems.append(f"T-{ident:03d}: slug {task.slug!r} is not filename-safe")
            if not EST.match(task.est):
                problems.append(f"T-{ident:03d}: est {task.est!r} does not match 'N-M min'")
            if not task.goal or len(task.goal) < 40:
                problems.append(f"T-{ident:03d}: goal is missing or too thin to act on")
            if len(task.skills) < 2:
                problems.append(f"T-{ident:03d}: needs at least two skills, has {len(task.skills)}")
            if not task.deliverables:
                problems.append(f"T-{ident:03d}: no deliverables")
            if len(task.steps) < 2:
                problems.append(f"T-{ident:03d}: fewer than two steps")
            if len(task.accept) < 2:
                problems.append(f"T-{ident:03d}: fewer than two acceptance criteria")
            if not task.verify:
                problems.append(f"T-{ident:03d}: no verification command")
            if not task.state:
                problems.append(f"T-{ident:03d}: no stated end state")
            for dep in task.deps:
                if dep == ident:
                    problems.append(f"T-{ident:03d}: depends on itself")
                elif dep not in tasks:
                    problems.append(f"T-{ident:03d}: dependency T-{dep:03d} does not exist")
                elif dep > ident:
                    problems.append(f"T-{ident:03d}: dependency T-{dep:03d} points forward")

    # dependencies that point at a task defined later in the file order are impossible
    for ident in order:
        for dep in tasks[ident].deps:
            if dep in phase_of and phase_of[dep] > phase_of[ident]:
                problems.append(f"T-{ident:03d}: depends on a later phase (T-{dep:03d})")

    total = len(tasks)

    # 4 — every referenced task id exists; a task nobody references is reported
    referenced: set[int] = set()
    documents: list[Path] = []
    for name in DOC_FILES:
        path = ROOT / name
        if path.exists():
            documents.append(path)
    for directory in DOC_DIRS:
        base = ROOT / directory
        if base.exists():
            documents.extend(sorted(base.rglob("*.md")))

    for path in documents:
        rel = str(path.relative_to(ROOT))
        if rel in SKIP_DOCS:
            continue
        text = path.read_text(encoding="utf-8")
        for match in TASK_REF.findall(text):
            ident = int(match)
            referenced.add(ident)
            if ident not in tasks:
                problems.append(f"{rel} references T-{ident:03d}, which does not exist")

    unreferenced = [ident for ident in order if ident not in referenced]

    # 5 — stated counts match reality
    phase_count = len(phases)
    for path in documents:
        rel = str(path.relative_to(ROOT))
        if rel in SKIP_DOCS:
            continue
        for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
            for pattern, kind in zip(COUNT_CLAIMS, ("tasks", "tasks+phases", "tasks", "tasks")):
                for groups in pattern.findall(line):
                    claimed = int(groups[0] if isinstance(groups, tuple) else groups)
                    if claimed != total:
                        problems.append(f"{rel}:{number}: claims {claimed} tasks, plan has {total}")
                    if kind == "tasks+phases" and int(groups[1]) != phase_count:
                        problems.append(
                            f"{rel}:{number}: claims {groups[1]} phases, plan has {phase_count}"
                        )

    # 6 — the kick-off file and its code word
    kickoff = ROOT / "KICKOFF.md"
    code_word = ""
    if not kickoff.exists():
        problems.append("KICKOFF.md is missing — the owner has no entry point to hand to an agent")
    else:
        match = re.search(r"\*\*Codewort:\*\*\s*`([^`]+)`", kickoff.read_text(encoding="utf-8"))
        if not match:
            problems.append("KICKOFF.md declares no code word in the expected form")
        else:
            code_word = match.group(1)
            readme = (ROOT / "README.md").read_text(encoding="utf-8")
            if code_word not in readme:
                problems.append(f"the code word {code_word!r} is not reachable from README.md")
            for claim in re.findall(r"\b(\d{3})\s+[Tt]asks?\b", kickoff.read_text(encoding="utf-8")):
                if int(claim) != total:
                    problems.append(f"KICKOFF.md claims {claim} tasks, plan has {total}")

    # composed checks — logic lives in the other tools, this one only reports
    composed_ok = True
    for command in (
        ["python3", "tools/generate_plan.py", "--check"],
        ["python3", "tools/check_links.py"],
        ["python3", "tools/check_skills.py"],
        ["python3", "tools/check_design_slop.py"],
        ["python3", "tools/check_design_slop.py", "--self-test"],
    ):
        if not args.quiet:
            print(f"  → {' '.join(command)}")
        composed_ok &= run(command)

    if not composed_ok:
        problems.append("a composed checker reported a problem (see above)")

    for line in warnings:
        print(f"WARN  {line}")

    if not args.quiet:
        print(f"\n  plan: {len(phases)} phases, {total} tasks, T-001 … T-{max(order):03d}")
        print(f"  ids referenced from documents: {len(referenced)} of {total}")
        if code_word:
            print(f"  code word: {code_word}")

    if unreferenced:
        print(
            f"WARN  {len(unreferenced)} task(s) are reachable only through plan/INDEX.md "
            "(no narrative document cross-references them): "
            + ", ".join(f"T-{i:03d}" for i in unreferenced)
        )

    if problems:
        print(f"\n{len(problems)} problem(s):")
        for line in problems:
            print(f"  FAIL  {line}")
        return 1

    print(f"\nplan is consistent — {total} tasks in {len(phases)} phases, nothing contradictory found")
    return 0


if __name__ == "__main__":
    sys.exit(main())
