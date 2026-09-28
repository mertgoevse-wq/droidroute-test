# T-200 — README gallery that cannot go stale

> Phase 16 · Visual evidence & launch · **Depends on:** T-197, T-199 · **Parallel-safe:** yes · **Est. agent time:** 120-240 min

## Goal

Put the real screenshots in the README, generated from the files on disk, with a check that fails when an image no longer matches what the app produces.

## Design contract (binding for this phase)

This phase produces images of the interface, so the design rules apply to the *evidence* as much as to the app: [docs/14-design-system.md](../../docs/14-design-system.md) §11–§12.

1. **A screenshot is evidence, not marketing.** It shows the real app in a real state. No mock-up passed off as a build, no cropped-away failure, no invented number in a pixel.
2. **Deterministic or worthless.** Same locale, same font scale, same device size, same seeded data — otherwise two people comparing images compare different things.
3. **Both modes, every state.** Dark and light, and the states that are hard to reach: empty, loading, error, offline, parked key.
4. **Name what is wrong in the image.** A screenshot review that finds nothing is either a perfect screen or a shallow review; the second is far more likely. Findings get a name, a cause and an after-picture.
5. **Images live in the repository.** Committed under `design/`, referenced from the README, and checked for staleness by CI — a linked image that no longer matches the app is a false claim.

## Read first (context budget)

- [`status/NEXT.md`](../../status/NEXT.md) — the next task and the pre-flight commands
- [`status/ERRORS.md`](../../status/ERRORS.md) — must have no open entry for this task
- [`handbooks/09-skill-resolution.md`](../../handbooks/09-skill-resolution.md) — what each skill label below means on this machine
- [`docs/11-tbc-resolutions.md`](../../docs/11-tbc-resolutions.md) — decisions already settled; not re-opened
- this file, top to bottom, plus the *Acceptance criteria* of every `Depends on` task

Do not read the rest of the plan to "get oriented" — the entry point is this file plus the documents linked here. If the work genuinely needs another document, read that one and nothing more.

## Skills (≥2 in parallel via subagents)

| Skill | Subagent role |
|---|---|
| `visual-qa` | choosing images that show the product honestly, including one that is not flattering |
| `ci-cd-github-actions` | generated sections and the staleness check that keeps them true |

Verification is never skipped. If you substitute a skill, log it — see [handbooks/02-subagent-orchestration.md](../../handbooks/02-subagent-orchestration.md).

## Deliverables

- A gallery section in `README.md` with committed screenshots (dark and light), the signal path, and one honest state
- `scripts/gallery.sh` regenerating the section, and a CI check that the committed section matches the images

## Steps

1. Pick images by what they show, not by how impressive they look. Include one state that is not success.
2. Generate the section from `design/screenshots/` so it cannot list an image that does not exist.
3. Keep the images small enough to keep the repository pleasant (compress, fixed width, one format).
4. Add the staleness check to CI: if the gallery and the files disagree, the build fails with the regeneration command.

## Acceptance criteria

- [ ] Every image referenced in the gallery exists in the repository
- [ ] The gallery shows both modes and at least one non-success state
- [ ] CI fails when the gallery is out of date (proven once, then reverted)
- [ ] Total image weight stays within the budget stated in the section

## Verification

```bash
bash scripts/gallery.sh --check
python3 tools/check_links.py
```

## Definition of done

- [ ] Every acceptance criterion above is ticked **and** was actually run
- [ ] The *Verification* commands above passed unmodified (pasting a raw result into `logs/tasks/T-200.log`)
- [ ] No placeholder, no invented endpoint/URL/model/field, no edit outside the files this task names
- [ ] Nothing was weakened to make a check pass (no deleted test, no raised threshold, no disabled rule)
- [ ] `status/PROGRESS.md` and `status/NEXT.md` updated in the same commit as the work
- [ ] `scripts/preflight-secrets.sh` clean
- [ ] UI work only: `python3 tools/check_design_slop.py` passes and the four craft tests ran ([docs/14-design-system.md](../../docs/14-design-system.md) §11)

## Rules that always apply

- Prohibitions and the quality bar: [handbooks/07-anti-slop-rules.md](../../handbooks/07-anti-slop-rules.md) (placeholders, invented endpoints, unrequested scope, weakened checks)
- At least two skills **in parallel** as subagents, one of them verification: [AGENTS.md](../../AGENTS.md) §4
- Log every meaningful step, commit and push exactly once for this task: [handbooks/05-logging-standard.md](../../handbooks/05-logging-standard.md) · [handbooks/04-git-protocol.md](../../handbooks/04-git-protocol.md)
- No secret in the repository, ever: `scripts/preflight-secrets.sh` must pass
- A new dependency, a deviation, or a settled decision goes into [status/DECISIONS.md](../../status/DECISIONS.md) in the same commit
- Missing tool for the job? Search before improvising: [handbooks/08-tooling-discovery.md](../../handbooks/08-tooling-discovery.md)

## Logging & Git

Protocols: [handbooks/04-git-protocol.md](../../handbooks/04-git-protocol.md) · [handbooks/05-logging-standard.md](../../handbooks/05-logging-standard.md)

- `scripts/log-step.sh T-200 "<action>" "<result>"` after every meaningful step
- `scripts/log-step.sh T-200 "test" "<command>" "pass" --actor verify` for each verification run
- Once every criterion above is ticked: `scripts/step-commit.sh "T-200: README gallery that cannot go stale"`
- Update [status/PROGRESS.md](../../status/PROGRESS.md) and [status/NEXT.md](../../status/NEXT.md) in the same commit

## State after success

Anyone opening the repository sees the real app — and the images cannot quietly become fiction.

## Stop conditions

Stop and report — do not improvise around these:

- A criterion fails after one honest repair attempt → append to [status/ERRORS.md](../../status/ERRORS.md) and stop the chain.
- This task contradicts [docs/11-tbc-resolutions.md](../../docs/11-tbc-resolutions.md) → the task is wrong: fix this file, log why, continue.
- A user-visible decision is needed that no document settles → stop and ask, naming the decision and the options.
- A provider's documentation or endpoint is unreachable → record exactly what was tried. **Never invent a URL, a model id or a field name.**
- The same environmental failure happens twice → stop; the third attempt is guessing.

## Handover

If this task is interrupted, append a `STOPPED:` note to [status/ERRORS.md](../../status/ERRORS.md) (template in [handbooks/06-resume-protocol.md](../../handbooks/06-resume-protocol.md)) describing the last completed step, the state of the working tree, and the next action. The next agent resumes from `logs/tasks/T-200.log`.
