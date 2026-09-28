# T-095 — Daily and weekly usage views

> Phase 07 · UI · **Depends on:** T-094, T-081 · **Parallel-safe:** yes · **Est. agent time:** 60-120 min

## Goal

Show token consumption and estimated cost per provider for today and the last seven days.

## Design contract (binding for this phase)

Every task in this phase produces something a person looks at, so the craft rules apply as strictly as the functional ones. Read [docs/14-design-system.md](../../docs/14-design-system.md) before writing a composable, and load the `design-craft` skill alongside the skills listed on the task.

**The direction, in one line:** a graphite instrument panel with hairline borders, one copper accent for the single primary action, real status lamps, and the request path made visible. Not a dark SaaS dashboard, not glass, not gradients. The mark is "Signal" and the asset sources live in [`design/`](../../design/README.md). The banned list is binding: [handbooks/07-anti-slop-rules.md](../../handbooks/07-anti-slop-rules.md) §11.

Before writing any composable:

1. **Name the focal element of the screen** and how it wins (size, weight, contrast, space). If you cannot name it, the screen is a list and should look like one. [docs/14 §8](../../docs/14-design-system.md)
2. **Use a token for every colour, space, radius and type role** from `ui/theme/Tokens.kt`. A value that does not exist yet is added to the token file first, with its reason, in the same commit.
3. **Hierarchy comes from size + weight + colour together**, never size alone. Contrast is not a substitute for hierarchy.
4. **Centering is an accent, not a default:** allowed for the onboarding hero, empty states and a single large metric. Body text, list rows, labels, settings and log lines stay left-aligned.
5. **Numbers are platform monospace with tabular figures** so a counting value does not shift its neighbours.
6. **Depth is borders only** — no shadow, no elevation, no blur, no glow.
7. **Every screen ships its states:** loading, empty, error, partial, offline, plus disabled states with a reason. A screen that only works when everything succeeds is not finished.
8. **Motion must explain something** and stays under 300 ms. Reduced motion removes movement, never information.

Before declaring the task done, run the four craft tests from [docs/14 §11](../../docs/14-design-system.md): **Swap** (would a stock template look the same?), **Squint** (is the hierarchy still readable, is nothing shouting?), **Signature** (point at five places where the product's idea appears), **Token** (do the token names belong to this product?). Then `python3 tools/check_design_slop.py` — a passing gate is necessary, not sufficient.

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
| `android-compose-ui` | simple, readable charts without a heavy charting dependency |
| `kotlin-core` | aggregation queries and caching that stay cheap on a phone |

Verification is never skipped. If you substitute a skill, log it — see [handbooks/02-subagent-orchestration.md](../../handbooks/02-subagent-orchestration.md).

## Deliverables

- `ui/dashboard/UsageSection.kt` with a 7-day view and a per-provider breakdown
- Cost shown as estimated, explicitly labelled when prices are unknown

## Steps

1. Aggregate from the usage table with a bounded query (indexed by timestamp).
2. Apply the chart rules from docs/14 §9: one accent series plus at most one comparison hue, zero-baseline bars, direct labels before a legend, tabular monospace figures.
3. Show free providers with an explicit '0 (free)' rather than hiding them.
4. Mark estimates as estimates and render an unknown price as *unknown* (hatched, labelled) — never a fabricated number.
5. Draw the bars on a canvas sized by Compose; colour them from the tokens. No charting dependency.
6. Add a test comparing the aggregate with a hand-computed fixture.

## Acceptance criteria

- [ ] The aggregate matches a fixture dataset exactly
- [ ] No chart shows more than two series, contains a gradient fill, a 3D effect or a non-zero baseline
- [ ] Unknown pricing is labelled and hatched, not filled with a fabricated number
- [ ] The query stays under 50 ms for a month of records (measured)

## Verification

```bash
./gradlew :app:testDebugUnitTest --tests '*UsageAggregat*'
```

## Definition of done

- [ ] Every acceptance criterion above is ticked **and** was actually run
- [ ] The *Verification* commands above passed unmodified (pasting a raw result into `logs/tasks/T-095.log`)
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

- `scripts/log-step.sh T-095 "<action>" "<result>"` after every meaningful step
- `scripts/log-step.sh T-095 "test" "<command>" "pass" --actor verify` for each verification run
- Once every criterion above is ticked: `scripts/step-commit.sh "T-095: Daily and weekly usage views"`
- Update [status/PROGRESS.md](../../status/PROGRESS.md) and [status/NEXT.md](../../status/NEXT.md) in the same commit

## State after success

Consumption is visible per provider and day, with costs labelled honestly.

## Stop conditions

Stop and report — do not improvise around these:

- A criterion fails after one honest repair attempt → append to [status/ERRORS.md](../../status/ERRORS.md) and stop the chain.
- This task contradicts [docs/11-tbc-resolutions.md](../../docs/11-tbc-resolutions.md) → the task is wrong: fix this file, log why, continue.
- A user-visible decision is needed that no document settles → stop and ask, naming the decision and the options.
- A provider's documentation or endpoint is unreachable → record exactly what was tried. **Never invent a URL, a model id or a field name.**
- The same environmental failure happens twice → stop; the third attempt is guessing.

## Handover

If this task is interrupted, append a `STOPPED:` note to [status/ERRORS.md](../../status/ERRORS.md) (template in [handbooks/06-resume-protocol.md](../../handbooks/06-resume-protocol.md)) describing the last completed step, the state of the working tree, and the next action. The next agent resumes from `logs/tasks/T-095.log`.
