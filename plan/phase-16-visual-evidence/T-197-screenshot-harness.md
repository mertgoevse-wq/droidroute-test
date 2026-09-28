# T-197 — Deterministic screenshot harness

> Phase 16 · Visual evidence & launch · **Depends on:** T-106, T-190 · **Parallel-safe:** yes · **Est. agent time:** 150-300 min

## Goal

Take screenshots that are worth comparing: fixed device sizes, fixed locale and font scale, seeded data, both modes, and every state that is hard to reach by hand.

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
| `visual-qa` | what a screenshot must contain to be evidence, and which states matter |
| `android-platform` | device control: screen capture, density, locale and font scale without hand-editing the device |

Verification is never skipped. If you substitute a skill, log it — see [handbooks/02-subagent-orchestration.md](../../handbooks/02-subagent-orchestration.md).

## Deliverables

- `scripts/shots.sh` — captures the matrix (screens × modes × sizes × states) into `design/screenshots/`
- A fixture mode that seeds deterministic data so numbers and timestamps do not change between runs
- A documented device matrix and the exact commands used

## Steps

1. Define the matrix: the five destinations plus onboarding and the explain sheet; dark and light; a phone width and a tablet width; the states each screen can be in.
2. Seed fixed data (a fixed provider list, fixed token counts, a fixed timestamp) so two runs are comparable.
3. Capture through the platform: `adb exec-out screencap` for real-device shots, and Compose screenshot tests where they are cheaper.
4. Pin locale, font scale and animation scale for the run, and restore them afterwards — the device is the owner's, not the harness's.
5. Name files predictably: `<screen>-<mode>-<state>-<width>.png`, and fail the script if a matrix entry produced no file.

## Acceptance criteria

- [ ] A single command reproduces the whole matrix, and a second run produces identical images for the same state
- [ ] Every hard-to-reach state (empty, loading, error, offline, parked) has a capture
- [ ] The device is left in its original configuration after the run (asserted by the script)
- [ ] A missing matrix entry fails the script instead of silently omitting an image

## Verification

```bash
bash scripts/shots.sh
ls design/screenshots | wc -l
```

## Definition of done

- [ ] Every acceptance criterion above is ticked **and** was actually run
- [ ] The *Verification* commands above passed unmodified (pasting a raw result into `logs/tasks/T-197.log`)
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

- `scripts/log-step.sh T-197 "<action>" "<result>"` after every meaningful step
- `scripts/log-step.sh T-197 "test" "<command>" "pass" --actor verify` for each verification run
- Once every criterion above is ticked: `scripts/step-commit.sh "T-197: Deterministic screenshot harness"`
- Update [status/PROGRESS.md](../../status/PROGRESS.md) and [status/NEXT.md](../../status/NEXT.md) in the same commit

## State after success

The interface can be looked at on demand, comparably, without touching the app by hand.

## Stop conditions

Stop and report — do not improvise around these:

- A criterion fails after one honest repair attempt → append to [status/ERRORS.md](../../status/ERRORS.md) and stop the chain.
- This task contradicts [docs/11-tbc-resolutions.md](../../docs/11-tbc-resolutions.md) → the task is wrong: fix this file, log why, continue.
- A user-visible decision is needed that no document settles → stop and ask, naming the decision and the options.
- A provider's documentation or endpoint is unreachable → record exactly what was tried. **Never invent a URL, a model id or a field name.**
- The same environmental failure happens twice → stop; the third attempt is guessing.

## Handover

If this task is interrupted, append a `STOPPED:` note to [status/ERRORS.md](../../status/ERRORS.md) (template in [handbooks/06-resume-protocol.md](../../handbooks/06-resume-protocol.md)) describing the last completed step, the state of the working tree, and the next action. The next agent resumes from `logs/tasks/T-197.log`.
