"""Data model for the DroidRoute build plan.

A Task carries only the substance (goal, steps, acceptance, evidence). The
structure — headings, links, commit protocol — is stamped by the renderer in
``tools/generate_plan.py`` so that all 190 files stay identical in shape.
"""

from dataclasses import dataclass, field
from typing import List, Sequence, Tuple

Skill = Tuple[str, str]  # (skill name, role of the subagent using it)


@dataclass(frozen=True)
class Task:
    id: int
    slug: str
    title: str
    goal: str
    deps: Sequence[int] = ()
    parallel: bool = True
    est: str = "20-60 min"
    skills: Sequence[Skill] = ()
    deliverables: Sequence[str] = ()
    steps: Sequence[str] = ()
    accept: Sequence[str] = ()
    verify: Sequence[str] = ()
    state: str = ""


@dataclass(frozen=True)
class Phase:
    number: int
    slug: str
    title: str
    summary: str
    tasks: Sequence[Task] = field(default_factory=tuple)
    design: str = ""
    """Phase-level design contract, rendered into every task of the phase.

    Only phases whose work has a visual surface set this. It lives here rather
    than in each task so the contract is stated once and cannot drift between
    sibling screens.
    """

    @property
    def folder(self) -> str:
        return f"phase-{self.number:02d}-{self.slug}"

    @property
    def id_range(self) -> str:
        if not self.tasks:
            return "—"
        return f"T-{self.tasks[0].id:03d} … T-{self.tasks[-1].id:03d}"


def task_filename(task: Task) -> str:
    return f"T-{task.id:03d}-{task.slug}.md"


def deps_label(task: Task) -> str:
    if not task.deps:
        return "— (entry task)"
    return ", ".join(f"T-{d:03d}" for d in task.deps)
