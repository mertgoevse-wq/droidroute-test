# T-201 — Launch video with the brag plugin

> Phase 16 · Visual evidence & launch · **Depends on:** T-200 · **Parallel-safe:** yes · **Est. agent time:** 150-300 min

## Goal

Produce the 15–25 second launch video with the installed `brag` plugin, from the real product and the real screenshots, with its poster frame in the README and the share copy in the release notes.

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
| `launch-video` | the brag workflow: hook, reveal, highlights, punchline, and the creative laws it enforces |
| `visual-qa` | making the video show the product truthfully rather than invent a product |

Verification is never skipped. If you substitute a skill, log it — see [handbooks/02-subagent-orchestration.md](../../handbooks/02-subagent-orchestration.md).

## Deliverables

- `brag-output/brag.mp4`, its poster `brag.jpg`, `share-copy.txt` and `brag-plan.md`
- The poster embedded in the README, and the video attached to a GitHub release

## Steps

1. Check the prerequisites and record their versions: Node 22+, FFmpeg on PATH, `npx hyperframes doctor`.
2. Run brag with a tone that matches this product (a serious, instrument-panel tone — not a parody), and let it read the real project code.
3. Verify the result against the creative laws: at least one scene shows the real interface, no generic SaaS claims, every readable line holds long enough to read.
4. Bake the poster as frame 0, embed it in the README, and attach the video to the release.
5. If the device cannot run the toolchain, run it in CI or on another machine, and say in the task log where it ran — do not describe a video that does not exist.

## Acceptance criteria

- [ ] The video exists, is 15–25 seconds, and shows the real interface at least once
- [ ] Its claims match the repository (no invented numbers, no feature that is not built)
- [ ] The poster is in the README and the video is attached to a release
- [ ] If it could not be produced here, the reason and the alternative location are recorded — and the README makes no video claim

## Verification

```bash
npx hyperframes doctor
ls -la brag-output/brag.mp4 brag-output/brag.jpg brag-output/share-copy.txt
```

## Definition of done

- [ ] Every acceptance criterion above is ticked **and** was actually run
- [ ] The *Verification* commands above passed unmodified (pasting a raw result into `logs/tasks/T-201.log`)
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

- `scripts/log-step.sh T-201 "<action>" "<result>"` after every meaningful step
- `scripts/log-step.sh T-201 "test" "<command>" "pass" --actor verify` for each verification run
- Once every criterion above is ticked: `scripts/step-commit.sh "T-201: Launch video with the brag plugin"`
- Update [status/PROGRESS.md](../../status/PROGRESS.md) and [status/NEXT.md](../../status/NEXT.md) in the same commit

## State after success

There is a shareable launch video made from the actual product, not from a description of it.

## Stop conditions

Stop and report — do not improvise around these:

- A criterion fails after one honest repair attempt → append to [status/ERRORS.md](../../status/ERRORS.md) and stop the chain.
- This task contradicts [docs/11-tbc-resolutions.md](../../docs/11-tbc-resolutions.md) → the task is wrong: fix this file, log why, continue.
- A user-visible decision is needed that no document settles → stop and ask, naming the decision and the options.
- A provider's documentation or endpoint is unreachable → record exactly what was tried. **Never invent a URL, a model id or a field name.**
- The same environmental failure happens twice → stop; the third attempt is guessing.

## Handover

If this task is interrupted, append a `STOPPED:` note to [status/ERRORS.md](../../status/ERRORS.md) (template in [handbooks/06-resume-protocol.md](../../handbooks/06-resume-protocol.md)) describing the last completed step, the state of the working tree, and the next action. The next agent resumes from `logs/tasks/T-201.log`.
