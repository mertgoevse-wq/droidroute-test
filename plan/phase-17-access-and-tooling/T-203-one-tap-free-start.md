# T-203 — One-tap free start with no account

> Phase 17 · One-tap access, key issuing & tooling coverage · **Depends on:** T-096, T-105, T-169 · **Parallel-safe:** yes · **Est. agent time:** 120-240 min

## Goal

Get a working gateway with one button and no sign-up: probe the bundled no-auth and free-tier providers in a fixed order, validate with a real call, enable the first that answers, and say honestly what was picked and what its limits are.

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
| `droidroute-provider-manifest` | which free providers exist, what they permit and how their limits are stated |
| `droidroute-verification` | a real validation call per candidate, and an honest failure when none works |

Verification is never skipped. If you substitute a skill, log it — see [handbooks/02-subagent-orchestration.md](../../handbooks/02-subagent-orchestration.md).

## Deliverables

- A `Gratis starten` action in onboarding and on the Dashboard's empty state
- A probe sequence with a per-candidate outcome, so a failure names every candidate and why it failed

## Steps

1. Order the candidates by the measured health and latency from earlier runs, not by a hardcoded preference.
2. Validate each candidate with a real, minimal call before enabling it — a provider that answers `/models` but not a completion is not working.
3. Show the chosen provider, its model and its stated limit right after success, with a link to change it.
4. If no candidate answers, say so with the per-candidate reasons and offer the manual path — never enable a provider that failed.
5. Record the outcome in the log so later free-tier decisions are based on evidence.

## Acceptance criteria

- [ ] On a fresh install, one tap reaches a verified working endpoint with no account and no key typed
- [ ] A failing candidate never becomes an enabled provider, and its reason is visible
- [ ] If every candidate fails, the screen states it and points at the manual path
- [ ] The free-tier limits shown match what the provider's response actually said

## Verification

```bash
./gradlew :app:testDebugUnitTest --tests '*FreeStart*'
curl -fsS http://127.0.0.1:8787/v1/models | head -20
```

## Definition of done

- [ ] Every acceptance criterion above is ticked **and** was actually run
- [ ] The *Verification* commands above passed unmodified (pasting a raw result into `logs/tasks/T-203.log`)
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

- `scripts/log-step.sh T-203 "<action>" "<result>"` after every meaningful step
- `scripts/log-step.sh T-203 "test" "<command>" "pass" --actor verify` for each verification run
- Once every criterion above is ticked: `scripts/step-commit.sh "T-203: One-tap free start with no account"`
- Update [status/PROGRESS.md](../../status/PROGRESS.md) and [status/NEXT.md](../../status/NEXT.md) in the same commit

## State after success

Starting costs one tap and no identity, and the app never pretends a dead provider works.

## Stop conditions

Stop and report — do not improvise around these:

- A criterion fails after one honest repair attempt → append to [status/ERRORS.md](../../status/ERRORS.md) and stop the chain.
- This task contradicts [docs/11-tbc-resolutions.md](../../docs/11-tbc-resolutions.md) → the task is wrong: fix this file, log why, continue.
- A user-visible decision is needed that no document settles → stop and ask, naming the decision and the options.
- A provider's documentation or endpoint is unreachable → record exactly what was tried. **Never invent a URL, a model id or a field name.**
- The same environmental failure happens twice → stop; the third attempt is guessing.

## Handover

If this task is interrupted, append a `STOPPED:` note to [status/ERRORS.md](../../status/ERRORS.md) (template in [handbooks/06-resume-protocol.md](../../handbooks/06-resume-protocol.md)) describing the last completed step, the state of the working tree, and the next action. The next agent resumes from `logs/tasks/T-203.log`.
