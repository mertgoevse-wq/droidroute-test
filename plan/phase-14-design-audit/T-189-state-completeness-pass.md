# T-189 — State completeness pass (loading, empty, error, partial, offline)

> Phase 14 · Design audit & release polish · **Depends on:** T-187 · **Parallel-safe:** yes · **Est. agent time:** 120-240 min

## Goal

Give every data-bearing screen its missing states, because the default path is the only one that ever gets built, and a gateway with no traffic shows nothing at all.

## Design contract (binding for this phase)

This phase audits; it does not redesign. The direction is already decided in [docs/14-design-system.md](../../docs/14-design-system.md) and the interface already exists — your job is to find where the build drifted from the system, prove it, and correct it.

Rules for every task in this phase:

1. **A finding needs a name, a cause and an after-picture.** "Looks better now" is not a finding. `docs/14` has a name for every defect class: flat hierarchy, monotone layout, harsh border, dramatic surface jump, mixed depth strategy, decorative layer, missing state, colour-only signal, off-scale value.
2. **Fix by moving back to the system, not by inventing a second system.** A failure is repaired by correcting a token or a layout decision. A new token needs its reason written down.
3. **Do not flatten the direction.** Removing the brass accent, quieting the signal path or neutering the density is not a fix — it is a different, worse product. [handbooks/07-anti-slop-rules.md](../../handbooks/07-anti-slop-rules.md) §11.
4. **Measure instead of asserting.** Contrast ratios, hit areas, query times and counts get numbers with the method stated. An unverifiable improvement claim is a violation (handbook rule 8).
5. **Leave what works alone.** The removal test decides: name the element's job, remove it mentally, and keep it if information would be lost.
6. **Name what is still not good.** Each task ends with residual weaknesses, stated plainly, rather than a claim of a clean finish.

The gate `python3 tools/check_design_slop.py` must pass at the end of every task here, and `--self-test` must pass in each task that touches the gate itself.

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
| `android-compose-ui` | state families in Compose without duplicating layout per branch |
| `droidroute-verification` | each state produced on the device, not simulated in a preview |

Verification is never skipped. If you substitute a skill, log it — see [handbooks/02-subagent-orchestration.md](../../handbooks/02-subagent-orchestration.md).

## Deliverables

- Five states implemented per data-bearing screen, demonstrated with a capture each
- Empty states that name the next action, error states in the API's own vocabulary

## Steps

1. Enumerate the screens that load data; for each, list which of the five states exist today.
2. Build the missing ones: skeletons in the shape of the real content, empty states that offer the action, errors that name the cause.
3. Make failures keep the last known value visible with a marker instead of blanking the screen.
4. Produce each state on the device (stop the server, revoke the key, cut the network) and capture it.

## Acceptance criteria

- [ ] Every data-bearing screen has all five states, each captured
- [ ] An empty Dashboard states the next action instead of showing zeros
- [ ] The offline state is reachable in airplane mode and still useful

## Verification

```bash
./gradlew :app:assembleDebug
adb shell cmd connectivity airplane-mode enable
```

## Definition of done

- [ ] Every acceptance criterion above is ticked **and** was actually run
- [ ] The *Verification* commands above passed unmodified (pasting a raw result into `logs/tasks/T-189.log`)
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

- `scripts/log-step.sh T-189 "<action>" "<result>"` after every meaningful step
- `scripts/log-step.sh T-189 "test" "<command>" "pass" --actor verify` for each verification run
- Once every criterion above is ticked: `scripts/step-commit.sh "T-189: State completeness pass (loading, empty, error, partial, offline)"`
- Update [status/PROGRESS.md](../../status/PROGRESS.md) and [status/NEXT.md](../../status/NEXT.md) in the same commit

## State after success

The interface is finished for the cases that actually happen, not only the happy one.

## Stop conditions

Stop and report — do not improvise around these:

- A criterion fails after one honest repair attempt → append to [status/ERRORS.md](../../status/ERRORS.md) and stop the chain.
- This task contradicts [docs/11-tbc-resolutions.md](../../docs/11-tbc-resolutions.md) → the task is wrong: fix this file, log why, continue.
- A user-visible decision is needed that no document settles → stop and ask, naming the decision and the options.
- A provider's documentation or endpoint is unreachable → record exactly what was tried. **Never invent a URL, a model id or a field name.**
- The same environmental failure happens twice → stop; the third attempt is guessing.

## Handover

If this task is interrupted, append a `STOPPED:` note to [status/ERRORS.md](../../status/ERRORS.md) (template in [handbooks/06-resume-protocol.md](../../handbooks/06-resume-protocol.md)) describing the last completed step, the state of the working tree, and the next action. The next agent resumes from `logs/tasks/T-189.log`.
