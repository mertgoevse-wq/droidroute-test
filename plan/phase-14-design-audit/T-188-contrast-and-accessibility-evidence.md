# T-188 — Measured contrast, motion and accessibility evidence

> Phase 14 · Design audit & release polish · **Depends on:** T-106 · **Parallel-safe:** yes · **Est. agent time:** 150-300 min

## Goal

Replace the assertion that contrast is fine with numbers: every foreground/background pair in both modes, plus TalkBack, 200 % font scale, reduced motion and touch targets, each with recorded evidence.

## Design contract (binding for this phase)

This phase audits; it does not redesign. The direction is already decided in [docs/14-design-system.md](../../docs/14-design-system.md) and the interface already exists — your job is to find where the build drifted from the system, prove it, and correct it.

Rules for every task in this phase:

1. **A finding needs a name, a cause and an after-picture.** "Looks better now" is not a finding. `docs/14` has a name for every defect class: flat hierarchy, monotone layout, harsh border, dramatic surface jump, mixed depth strategy, decorative layer, missing state, colour-only signal, off-scale value.
2. **Fix by moving back to the system, not by inventing a second system.** A failure is repaired by correcting a token or a layout decision. A new token needs its reason written down.
3. **Do not flatten the direction.** Removing the copper accent, quieting the signal path or neutering the density is not a fix — it is a different, worse product. [handbooks/07-anti-slop-rules.md](../../handbooks/07-anti-slop-rules.md) §11.
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
| `design-a11y` | WCAG thresholds and how a failure is fixed without flattening the direction |
| `droidroute-verification` | measured ratios, screen-reader transcripts, font-scale captures |

Verification is never skipped. If you substitute a skill, log it — see [handbooks/02-subagent-orchestration.md](../../handbooks/02-subagent-orchestration.md).

## Deliverables

- A contrast table: token pair → measured ratio → threshold → pass/fail, both modes
- Evidence for TalkBack descriptions, 200 % font scale, reduced motion and hit areas

## Steps

1. Compute the ratio for every pair actually used; record the measured value, not a rounded claim.
2. Fix failures by adjusting the token, never by moving text off a surface or dropping a level of the hierarchy.
3. Run the whole app with TalkBack: every control described, the signal path announced as words.
4. Set the animation scale to 0 and confirm the Signalweg is static, readable and still truthful.
5. Test at 200 % font scale; fix truncation, overlap and clipped controls.

## Acceptance criteria

- [ ] Every used pair meets its threshold, with the measured ratio recorded
- [ ] Reduced motion removes movement and keeps every piece of information
- [ ] No screen breaks at 200 % font scale, and every control is reachable with the screen reader

## Verification

```bash
./gradlew :app:lintDebug
adb shell settings put global animator_duration_scale 0
adb shell settings put global animator_duration_scale 1
```

## Definition of done

- [ ] Every acceptance criterion above is ticked **and** was actually run
- [ ] The *Verification* commands above passed unmodified (pasting a raw result into `logs/tasks/T-188.log`)
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

- `scripts/log-step.sh T-188 "<action>" "<result>"` after every meaningful step
- `scripts/log-step.sh T-188 "test" "<command>" "pass" --actor verify` for each verification run
- Once every criterion above is ticked: `scripts/step-commit.sh "T-188: Measured contrast, motion and accessibility evidence"`
- Update [status/PROGRESS.md](../../status/PROGRESS.md) and [status/NEXT.md](../../status/NEXT.md) in the same commit

## State after success

Accessibility is a measurement in this repository, not an intention.

## Stop conditions

Stop and report — do not improvise around these:

- A criterion fails after one honest repair attempt → append to [status/ERRORS.md](../../status/ERRORS.md) and stop the chain.
- This task contradicts [docs/11-tbc-resolutions.md](../../docs/11-tbc-resolutions.md) → the task is wrong: fix this file, log why, continue.
- A user-visible decision is needed that no document settles → stop and ask, naming the decision and the options.
- A provider's documentation or endpoint is unreachable → record exactly what was tried. **Never invent a URL, a model id or a field name.**
- The same environmental failure happens twice → stop; the third attempt is guessing.

## Handover

If this task is interrupted, append a `STOPPED:` note to [status/ERRORS.md](../../status/ERRORS.md) (template in [handbooks/06-resume-protocol.md](../../handbooks/06-resume-protocol.md)) describing the last completed step, the state of the working tree, and the next action. The next agent resumes from `logs/tasks/T-188.log`.
