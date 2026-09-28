# T-194 — Network surface and exposure audit

> Phase 15 · Security & privacy audit · **Depends on:** T-014, T-021, T-165 · **Parallel-safe:** yes · **Est. agent time:** 120-240 min

## Goal

Prove the exposure model: every combination of bind mode and auth mode has a test, upstream calls verify TLS, and nothing leaks version or configuration in an error.

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
| `security-audit` | the exposure matrix and what a reachable port actually exposes |
| `ktor-server` | server hardening: timeouts, body limits, error shapes, no banner |

Verification is never skipped. If you substitute a skill, log it — see [handbooks/02-subagent-orchestration.md](../../handbooks/02-subagent-orchestration.md).

## Deliverables

- An exposure matrix (bind × auth × reachability) with a test per row
- Proof that TLS verification is on for every upstream provider and that cleartext to a non-local host is refused

## Steps

1. Test that a non-loopback bind without a key is refused, and that the refusal is the same whether or not the port answers.
2. Verify certificate verification for all upstream calls and that no trust-all setting exists anywhere.
3. Refuse plaintext `http://` to a non-loopback provider unless the owner explicitly opted in for a local address.
4. Set bounded request sizes and timeouts; confirm an oversized body is rejected rather than buffered.
5. Check that error bodies and headers leak no version, build id, provider key fragment or internal path.

## Acceptance criteria

- [ ] Every matrix row has a passing test
- [ ] A non-local bind without a key is refused (asserted)
- [ ] Cleartext to a public host is refused (asserted)
- [ ] No error body contains a version string, an internal path or a credential fragment

## Verification

```bash
./gradlew :app:testDebugUnitTest --tests '*Exposure*'
curl -fsS http://127.0.0.1:8787/health
```

## Definition of done

- [ ] Every acceptance criterion above is ticked **and** was actually run
- [ ] The *Verification* commands above passed unmodified (pasting a raw result into `logs/tasks/T-194.log`)
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

- `scripts/log-step.sh T-194 "<action>" "<result>"` after every meaningful step
- `scripts/log-step.sh T-194 "test" "<command>" "pass" --actor verify` for each verification run
- Once every criterion above is ticked: `scripts/step-commit.sh "T-194: Network surface and exposure audit"`
- Update [status/PROGRESS.md](../../status/PROGRESS.md) and [status/NEXT.md](../../status/NEXT.md) in the same commit

## State after success

Exposure is a table with tests behind it, not an assumption about the default.

## Stop conditions

Stop and report — do not improvise around these:

- A criterion fails after one honest repair attempt → append to [status/ERRORS.md](../../status/ERRORS.md) and stop the chain.
- This task contradicts [docs/11-tbc-resolutions.md](../../docs/11-tbc-resolutions.md) → the task is wrong: fix this file, log why, continue.
- A user-visible decision is needed that no document settles → stop and ask, naming the decision and the options.
- A provider's documentation or endpoint is unreachable → record exactly what was tried. **Never invent a URL, a model id or a field name.**
- The same environmental failure happens twice → stop; the third attempt is guessing.

## Handover

If this task is interrupted, append a `STOPPED:` note to [status/ERRORS.md](../../status/ERRORS.md) (template in [handbooks/06-resume-protocol.md](../../handbooks/06-resume-protocol.md)) describing the last completed step, the state of the working tree, and the next action. The next agent resumes from `logs/tasks/T-194.log`.
