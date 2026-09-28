# T-204 — One-tap sign-in with the device code flow

> Phase 17 · One-tap access, key issuing & tooling coverage · **Depends on:** T-057, T-171 · **Parallel-safe:** yes · **Est. agent time:** 150-300 min

## Goal

Sign in to the providers that support it with one tap — show a short code, the owner confirms on a page, done — instead of hunting for an API key. Where a provider has no such flow, say so and fall back without pretending.

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
| `oauth-device-flow` | the real device-authorization flow, its polling rules and its error states |
| `ai-governors` | a login that silently uses an account would be a defect — the owner confirms, always |

Verification is never skipped. If you substitute a skill, log it — see [handbooks/02-subagent-orchestration.md](../../handbooks/02-subagent-orchestration.md).

## Deliverables

- A reusable device-code sign-in that onboarding, the provider list and provider detail can all open
- The sign-in screen: the code, a copy action, the verification address, remaining time, and a cancel that actually stops the polling

## Steps

1. Implement the flow once and reuse it: request a code, show it, poll at the interval the provider specified, handle slow-down and expiry.
2. Store the result in the vault under the account's label, never in a shared blob, and name the account so multi-account rotation (T-171) applies.
3. Handle the honest failures: expired code, denied consent, no such flow, offline.
4. State on screen what the sign-in grants and what it does not, before the owner confirms.
5. Cancel must stop the polling immediately, with no background attempt afterwards.

## Acceptance criteria

- [ ] Signing in from onboarding takes one tap plus one confirmation on a page (demonstrated once)
- [ ] Expired and denied flows show a precise message and leave no half-configured account
- [ ] Cancel stops all network activity for that flow (verified in the log)
- [ ] A provider without this flow is labelled as such and offers the key path instead

## Verification

```bash
./gradlew :app:testDebugUnitTest --tests '*DeviceCode*'
python3 tools/check_plan_consistency.py
```

## Definition of done

- [ ] Every acceptance criterion above is ticked **and** was actually run
- [ ] The *Verification* commands above passed unmodified (pasting a raw result into `logs/tasks/T-204.log`)
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

- `scripts/log-step.sh T-204 "<action>" "<result>"` after every meaningful step
- `scripts/log-step.sh T-204 "test" "<command>" "pass" --actor verify` for each verification run
- Once every criterion above is ticked: `scripts/step-commit.sh "T-204: One-tap sign-in with the device code flow"`
- Update [status/PROGRESS.md](../../status/PROGRESS.md) and [status/NEXT.md](../../status/NEXT.md) in the same commit

## State after success

Accounts are connected by confirming a code, not by copying a secret into a text field.

## Stop conditions

Stop and report — do not improvise around these:

- A criterion fails after one honest repair attempt → append to [status/ERRORS.md](../../status/ERRORS.md) and stop the chain.
- This task contradicts [docs/11-tbc-resolutions.md](../../docs/11-tbc-resolutions.md) → the task is wrong: fix this file, log why, continue.
- A user-visible decision is needed that no document settles → stop and ask, naming the decision and the options.
- A provider's documentation or endpoint is unreachable → record exactly what was tried. **Never invent a URL, a model id or a field name.**
- The same environmental failure happens twice → stop; the third attempt is guessing.

## Handover

If this task is interrupted, append a `STOPPED:` note to [status/ERRORS.md](../../status/ERRORS.md) (template in [handbooks/06-resume-protocol.md](../../handbooks/06-resume-protocol.md)) describing the last completed step, the state of the working tree, and the next action. The next agent resumes from `logs/tasks/T-204.log`.
