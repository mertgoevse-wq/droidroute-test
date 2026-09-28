# T-191 — Threat model and test mapping

> Phase 15 · Security & privacy audit · **Depends on:** T-014, T-021, T-165 · **Parallel-safe:** yes · **Est. agent time:** 150-300 min

## Goal

Write the threat model against what was actually built — assets, entry points, trust boundaries, attacker capabilities — and map every threat to an existing test, a missing test, or an explicitly accepted risk.

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
| `security-audit` | assets, boundaries, attacker capability and the honest classification of residual risk |
| `technical-writing` | a model a reader can act on, not a taxonomy exercise |

Verification is never skipped. If you substitute a skill, log it — see [handbooks/02-subagent-orchestration.md](../../handbooks/02-subagent-orchestration.md).

## Deliverables

- `docs/16-threat-model.md`: assets, entry points, trust boundaries, attacker profiles, threat table
- A mapping table: threat → control → test (or → accepted risk with the reason and the owner's decision)

## Steps

1. Enumerate assets: provider keys, subscription tokens, client keys, request content, logs, local model files, the vault itself.
2. Enumerate entry points: the four protocol surfaces, the admin API, the share sheet, deep links, the MCP bridge, notifications.
3. Enumerate boundaries: app ↔ internet, app ↔ other apps, agent ↔ gateway, device ↔ LAN/tunnel.
4. For each threat, name the control that exists and the test that proves it. Where a test does not exist, record it as a task — do not imply coverage.
5. State accepted risks explicitly with the reason (for example: a rooted device, memory while running, a malicious accessibility service).

## Acceptance criteria

- [ ] Every asset has a control or an explicitly accepted risk
- [ ] Every entry point has an authentication and an input-validation decision
- [ ] Every threat row names a test, a new task id, or an accepted risk — no empty cells
- [ ] The model names what is *not* protected, in the same document

## Verification

```bash
python3 tools/check_plan_consistency.py
grep -rn 'TBD\|TODO\|to be decided' docs/16-threat-model.md || echo 'no unresolved markers'
```

## Definition of done

- [ ] Every acceptance criterion above is ticked **and** was actually run
- [ ] The *Verification* commands above passed unmodified (pasting a raw result into `logs/tasks/T-191.log`)
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

- `scripts/log-step.sh T-191 "<action>" "<result>"` after every meaningful step
- `scripts/log-step.sh T-191 "test" "<command>" "pass" --actor verify` for each verification run
- Once every criterion above is ticked: `scripts/step-commit.sh "T-191: Threat model and test mapping"`
- Update [status/PROGRESS.md](../../status/PROGRESS.md) and [status/NEXT.md](../../status/NEXT.md) in the same commit

## State after success

Security claims are checkable: every threat points at a test or at a decision the owner made.

## Stop conditions

Stop and report — do not improvise around these:

- A criterion fails after one honest repair attempt → append to [status/ERRORS.md](../../status/ERRORS.md) and stop the chain.
- This task contradicts [docs/11-tbc-resolutions.md](../../docs/11-tbc-resolutions.md) → the task is wrong: fix this file, log why, continue.
- A user-visible decision is needed that no document settles → stop and ask, naming the decision and the options.
- A provider's documentation or endpoint is unreachable → record exactly what was tried. **Never invent a URL, a model id or a field name.**
- The same environmental failure happens twice → stop; the third attempt is guessing.

## Handover

If this task is interrupted, append a `STOPPED:` note to [status/ERRORS.md](../../status/ERRORS.md) (template in [handbooks/06-resume-protocol.md](../../handbooks/06-resume-protocol.md)) describing the last completed step, the state of the working tree, and the next action. The next agent resumes from `logs/tasks/T-191.log`.
