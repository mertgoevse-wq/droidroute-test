# T-205 — DroidRoute key issuing, readable by nobody

> Phase 17 · One-tap access, key issuing & tooling coverage · **Depends on:** T-016, T-021, T-099, T-165, T-193 · **Parallel-safe:** yes · **Est. agent time:** 180-360 min

## Goal

Let the owner issue DroidRoute's own API keys — created on the device, stored only encrypted, shown exactly once, and unreadable afterwards by anyone, including the owner. No export path exists, by design.

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
| `security-audit` | a secret that cannot be read back needs its storage claims tested, not documented |
| `droidroute-verification` | proving the absence of a read-back path, which is harder than proving a feature works |

Verification is never skipped. If you substitute a skill, log it — see [handbooks/02-subagent-orchestration.md](../../handbooks/02-subagent-orchestration.md).

## Deliverables

- `ui/keys/IssueKeyScreen.kt` — scope, expiry, label, then one-time reveal
- `keys/Issuer.kt` — generation, hashing, scope enforcement, revocation, with no retrieval API
- A test suite that fails if any code path can reproduce a stored key

## Steps

1. Generate keys with a cryptographically secure source and store only what verification needs — never the key itself.
2. Show the full key exactly once, with an explicit "this is the only time you will see it" and a copy action that uses the 60-second clipboard timer.
3. Store afterwards only what is needed to mask (`first5••••last5`) — the mask is metadata, not the secret.
4. Support scope (models, read-only, budget, expiry) and revocation that takes effect without a restart.
5. Write the test that would catch a regression: search the storage layer and the API for any path that returns a stored key, and assert there is none.

## Acceptance criteria

- [ ] A newly issued key works against the gateway and appears masked afterwards
- [ ] After the one-time reveal, no API, screen, export or log can reproduce it (asserted by a test that fails if a read-back path is added)
- [ ] Revocation invalidates the key immediately (asserted)
- [ ] Scope and expiry are enforced, and a scoped key cannot exceed its scope (asserted)
- [ ] The documentation states plainly that a lost key is replaced, never recovered

## Verification

```bash
./gradlew :app:testDebugUnitTest --tests '*KeyIssuer*'
scripts/preflight-secrets.sh
```

## Definition of done

- [ ] Every acceptance criterion above is ticked **and** was actually run
- [ ] The *Verification* commands above passed unmodified (pasting a raw result into `logs/tasks/T-205.log`)
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

- `scripts/log-step.sh T-205 "<action>" "<result>"` after every meaningful step
- `scripts/log-step.sh T-205 "test" "<command>" "pass" --actor verify` for each verification run
- Once every criterion above is ticked: `scripts/step-commit.sh "T-205: DroidRoute key issuing, readable by nobody"`
- Update [status/PROGRESS.md](../../status/PROGRESS.md) and [status/NEXT.md](../../status/NEXT.md) in the same commit

## State after success

DroidRoute's own keys are usable by its clients and readable by nobody — enforced by tests, not by intent.

## Stop conditions

Stop and report — do not improvise around these:

- A criterion fails after one honest repair attempt → append to [status/ERRORS.md](../../status/ERRORS.md) and stop the chain.
- This task contradicts [docs/11-tbc-resolutions.md](../../docs/11-tbc-resolutions.md) → the task is wrong: fix this file, log why, continue.
- A user-visible decision is needed that no document settles → stop and ask, naming the decision and the options.
- A provider's documentation or endpoint is unreachable → record exactly what was tried. **Never invent a URL, a model id or a field name.**
- The same environmental failure happens twice → stop; the third attempt is guessing.

## Handover

If this task is interrupted, append a `STOPPED:` note to [status/ERRORS.md](../../status/ERRORS.md) (template in [handbooks/06-resume-protocol.md](../../handbooks/06-resume-protocol.md)) describing the last completed step, the state of the working tree, and the next action. The next agent resumes from `logs/tasks/T-205.log`.
