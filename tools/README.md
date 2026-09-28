# tools/ — how the plan is produced

`plan/` is **generated**. The task files are built from the phase data in `tools/plan_data/`, so the 208 tasks stay consistent in structure and can be edited in one place.

```
tools/
├── generate_plan.py       # writes plan/phase-*/T-*.md and plan/INDEX.md
├── check_links.py         # every relative markdown link resolves
├── check_skills.py        # every plan role label resolves to an installed skill/plugin/MCP server
├── check_design_slop.py   # the design gate from docs/14 (with --self-test)
├── check_plan_consistency.py  # composes the above and adds id/dep/count/doc invariants
├── plan_data/
│   ├── common.py          # Task + Phase dataclasses, renderer input
│   ├── phase_00.py … phase_17.py
└── README.md
```

## Regenerate

```bash
python3 tools/generate_plan.py            # write all task files + INDEX.md
python3 tools/generate_plan.py --check    # verify the files on disk match the data
python3 tools/generate_plan.py --phase 6  # only phase 6
python3 tools/check_links.py              # every relative markdown link resolves
python3 tools/check_skills.py             # every role label resolves to something installed
python3 tools/check_design_slop.py        # no banned aesthetic, no unmanaged value
python3 tools/check_plan_consistency.py   # the whole set, plus ids, deps, counts and the code word
```

`check_plan_consistency.py` is the one to run when something feels off: it calls the other four and
adds the invariants none of them own (unique ids, backwards-only dependencies, no empty task,
every `T-0xx` in the documents exists, every stated task count matches reality).

## Adding or changing a task

1. Edit the relevant `phase_XX.py`: adjust the `T(...)` entry, or append a new one.
2. Run `python3 tools/generate_plan.py --phase XX`.
3. Check the diff: a new task must not renumber existing ones (ids are explicit, never positional).
4. Commit the data change **and** the generated files in the same commit, message `plan: <what changed>`.

Renumbering is forbidden: commit messages, status files and logs reference task ids, so ids are stable identifiers, not positions.

## Why a generator

208 hand-written files drift — one task loses its acceptance criteria, another grows a third style of heading. The generator guarantees:

- every task has the same required sections (`Goal`, `Skills`, `Deliverables`, `Steps`, `Acceptance criteria`, `Verification`, `Logging & Git`, `State after success`),
- dependencies and phase membership are declared once,
- `plan/INDEX.md` can never disagree with the folder contents — and CI enforces exactly that (`repo-hygiene.yml` → *Plan integrity*).

Generated does not mean generic: every task's goal, steps, deliverables and acceptance criteria are written by hand in the phase data. The generator only stamps the structure.
