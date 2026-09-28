#!/usr/bin/env python3
"""Render the DroidRoute build plan from ``tools/plan_data``.

    python3 tools/generate_plan.py             # write everything
    python3 tools/generate_plan.py --check     # verify the tree matches the data
    python3 tools/generate_plan.py --phase 6   # only phase 06
    python3 tools/generate_plan.py --list      # print the task index

Task ids are explicit and stable: never renumber, or the commit history, status
files and logs will point at the wrong task.
"""

from __future__ import annotations

import argparse
import importlib.util
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PLAN_DIR = ROOT / "plan"
DATA_DIR = Path(__file__).resolve().parent / "plan_data"

sys.path.insert(0, str(DATA_DIR))

from common import Phase, Task, deps_label, task_filename  # noqa: E402


def load_phases() -> list[Phase]:
    phases: list[Phase] = []
    for path in sorted(DATA_DIR.glob("phase_*.py")):
        spec = importlib.util.spec_from_file_location(path.stem, path)
        if spec is None or spec.loader is None:  # pragma: no cover
            raise RuntimeError(f"cannot load {path}")
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        phase: Phase = module.PHASE
        tasks: list[Task] = list(module.TASKS)
        phases.append(Phase(phase.number, phase.slug, phase.title, phase.summary, tasks))
    phases.sort(key=lambda p: p.number)
    return phases


def render_task(phase: Phase, task: Task) -> str:
    skills = "\n".join(f"| `{name}` | {role} |" for name, role in task.skills)
    deliverables = "\n".join(f"- {d}" for d in task.deliverables)
    steps = "\n".join(f"{i}. {s}" for i, s in enumerate(task.steps, start=1))
    accept = "\n".join(f"- [ ] {a}" for a in task.accept)
    verify = "\n".join(task.verify)
    commit_msg = f"T-{task.id:03d}: {task.title}"

    return f"""# T-{task.id:03d} — {task.title}

> Phase {phase.number:02d} · {phase.title} · **Depends on:** {deps_label(task)} · \
**Parallel-safe:** {"yes" if task.parallel else "no"} · **Est. agent time:** {task.est}

## Goal

{task.goal}

## Skills (≥2 in parallel via subagents)

| Skill | Subagent role |
|---|---|
{skills}

Verification is never skipped. If you substitute a skill, log it — see \
[handbooks/02-subagent-orchestration.md](../../handbooks/02-subagent-orchestration.md).

## Deliverables

{deliverables}

## Steps

{steps}

## Acceptance criteria

{accept}

## Verification

```bash
{verify}
```

## Logging & Git

Protocols: [handbooks/04-git-protocol.md](../../handbooks/04-git-protocol.md) · \
[handbooks/05-logging-standard.md](../../handbooks/05-logging-standard.md)

- `scripts/log-step.sh T-{task.id:03d} "<action>" "<result>"` after every meaningful step
- `scripts/log-step.sh T-{task.id:03d} "test" "<command>" "pass" --actor verify` for each verification run
- Once every criterion above is ticked: `scripts/step-commit.sh "{commit_msg}"`
- Update [status/PROGRESS.md](../../status/PROGRESS.md) and [status/NEXT.md](../../status/NEXT.md) in the same commit

## State after success

{task.state}

## Handover

If this task is interrupted, append a `STOPPED:` note to [status/ERRORS.md](../../status/ERRORS.md) \
(template in [handbooks/06-resume-protocol.md](../../handbooks/06-resume-protocol.md)) describing the \
last completed step, the state of the working tree, and the next action. The next agent resumes from \
`logs/tasks/T-{task.id:03d}.log`.
"""


def render_index(phases: list[Phase]) -> str:
    total = sum(len(p.tasks) for p in phases)
    rows = []
    for phase in phases:
        rows.append(
            f"| [{phase.number:02d} — {phase.title}]({phase.folder}/) | {phase.id_range} | "
            f"{len(phase.tasks)} | {phase.summary} |"
        )
    phase_table = "\n".join(rows)

    sections = []
    for phase in phases:
        lines = [f"### Phase {phase.number:02d} — {phase.title}", "", phase.summary, ""]
        lines.append("| Task | Title | Depends on | Parallel |")
        lines.append("|---|---|---|---|")
        for task in phase.tasks:
            link = f"[T-{task.id:03d}]({phase.folder}/{task_filename(task)})"
            lines.append(
                f"| {link} | {task.title} | {deps_label(task)} | {'yes' if task.parallel else 'no'} |"
            )
        lines.append("")
        sections.append("\n".join(lines))

    return f"""# Build plan — {total} tasks

The execution order is the numeric order of the task ids. Each task is one commit
and one log file. Rules: [AGENTS.md](../AGENTS.md) · process: [docs/08-workflow.md](../docs/08-workflow.md) ·
resume: [handbooks/06-resume-protocol.md](../handbooks/06-resume-protocol.md).

**Start at [T-001](phase-00-foundation/T-001-repository-hygiene.md).** `status/NEXT.md` always names the next task.

| Phase | Tasks | Count | Focus |
|---|---|---|---|
{phase_table}

## All tasks

{chr(10).join(sections)}## Generated file

This index and every task file are produced by `tools/generate_plan.py` from `tools/plan_data/`.
Edit the data, run the generator, commit both. CI fails when the tree and the data disagree
(`.github/workflows/repo-hygiene.yml` → *Plan integrity*).
"""


def write(path: Path, content: str, check: bool) -> bool:
    if check:
        if not path.exists():
            print(f"MISSING  {path.relative_to(ROOT)}")
            return False
        if path.read_text(encoding="utf-8") != content:
            print(f"STALE    {path.relative_to(ROOT)}")
            return False
        return True
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    print(f"wrote    {path.relative_to(ROOT)}")
    return True


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="verify instead of writing")
    parser.add_argument("--phase", type=int, help="only this phase number")
    parser.add_argument("--list", action="store_true", help="print the task index and exit")
    args = parser.parse_args()

    phases = load_phases()
    if args.phase is not None:
        phases = [p for p in phases if p.number == args.phase]
        if not phases:
            print(f"no phase {args.phase} in the data", file=sys.stderr)
            return 2

    if args.list:
        for phase in phases:
            print(f"phase {phase.number:02d} — {phase.title} ({len(phase.tasks)} tasks)")
            for task in phase.tasks:
                print(f"  T-{task.id:03d}  {task.title}")
        return 0

    ok = True
    for phase in phases:
        for task in phase.tasks:
            path = PLAN_DIR / phase.folder / task_filename(task)
            ok &= write(path, render_task(phase, task), args.check)

    if args.phase is None or args.phase == 0:
        ok &= write(PLAN_DIR / "INDEX.md", render_index(phases), args.check)

    if args.check:
        if not ok:
            print("\nplan is out of date — run: python3 tools/generate_plan.py")
            return 1
        print("plan matches the data")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
