# AGENTS.md — operating rules (canonical)

Any agentic tool that builds this project reads this file. `CLAUDE.md` is the Claude Code entry point and defers to this document; do not duplicate rules in both.

## 1. What this repository is

The build plan for **DroidRoute**, an Android-native AI gateway. [`plan/`](plan/INDEX.md) contains **147 task files**. Your job is to execute them in numeric order — completely, verifiably, and without human intervention.

## 2. Boot sequence (no chat history assumed)

```
status/PROGRESS.md   → what is done
status/NEXT.md       → the next task id
status/DECISIONS.md  → decisions already settled (do not re-open)
status/ERRORS.md     → known breakage
logs/chain.log       → tail -n 80 for recent history
git status --short   → must be clean before you start
```

Details and edge cases: [`handbooks/06-resume-protocol.md`](handbooks/06-resume-protocol.md).

## 3. The task loop

For each task, in order:

1. Read the whole task file — including `Depends on` and `Acceptance criteria`.
2. Confirm dependencies by inspecting deliverables, not by trusting a checkbox.
3. Dispatch **at least two skills in parallel as subagents** (see §4).
4. Integrate; resolve conflicts deliberately, not by overwriting.
5. Run the task's **Verification** commands verbatim.
6. Log every meaningful step: `scripts/log-step.sh`.
7. On success: update `status/PROGRESS.md` + `status/NEXT.md`, then `scripts/step-commit.sh "T-0xx: <title>"`.
8. On failure: one honest repair attempt, then append to `status/ERRORS.md` and **stop the chain**.

Do not skip tasks. Do not reorder them for convenience. Do not batch several tasks into one commit.

## 4. Minimum two skills, in parallel, always

- Every task names ≥ 2 skills with roles. The default split is **implement / verify / document**.
- Verification is never optional and never skipped, even for a one-line change.
- The task's skill suggestion is a default **with freedom to deviate** — but never below two parallel workstreams.
- Subagents must not write the same file in the same round; serialise and log the reason if they must.
- Full pattern: [`handbooks/02-subagent-orchestration.md`](handbooks/02-subagent-orchestration.md) · catalog: [`handbooks/03-skills-catalog.md`](handbooks/03-skills-catalog.md).

## 5. Logging (everything)

Structured JSON-lines, redacted, in `logs/`. Every command, file write, verification result, error and deviation. Format: [`handbooks/05-logging-standard.md`](handbooks/05-logging-standard.md).

## 6. Git (always stage, commit, push)

```bash
scripts/step-commit.sh "T-0xx: <title>"        # commit + push
scripts/step-commit.sh --checkpoint "T-0xx"    # tag a rollback point first
```

One task = one commit. Subject is exactly `T-0xx: <task title>`. `main` only, never force-push. Push failure → keep the commit local, log it, retry at the next task boundary. Full protocol: [`handbooks/04-git-protocol.md`](handbooks/04-git-protocol.md).

## 7. Hard prohibitions

- **Never** commit a secret, key, token, keystore or `.env` content.
- **Never** invent a provider URL, model id, or API field — read the docs, or stop and record.
- **Never** commit placeholder or stub implementations.
- **Never** touch files outside the task's scope.
- **Never** weaken a test, lint rule or the secrets preflight to make a commit pass.
- **Never** force-push or rewrite history — history is the handover mechanism.

Full list with examples: [`handbooks/07-anti-slop-rules.md`](handbooks/07-anti-slop-rules.md).

## 8. Use the connected tooling

- **MCP servers, plugins and connectors that are available must be used.** DroidRoute federates them (`docs/07-mcp-plugins.md`); before writing a tool yourself, check `GET /mcp/tools`.
- Prefer an installed skill over a hand-rolled instruction; record substitutions in the task log.
- If a tool is unavailable, proceed with the task's documented degraded path and log it.

## 9. Stop conditions

Stop and report when: a criterion fails after one repair attempt; a user-visible decision is needed that the spec does not cover; the same environmental failure happens twice; or the task itself turns out to be wrong (then fix the plan file, log why, continue).

## 10. Canonical documents

| Question | File |
|---|---|
| Why does the app exist / scope | `docs/00-overview.md`, `docs/droidroute-spec.md` |
| How is it structured | `docs/01-architecture.md` |
| Which wire formats | `docs/02-protocols.md` |
| Which providers, how to add one | `docs/03-providers.md` |
| How requests are routed | `docs/04-routing.md` |
| Secrets and access control | `docs/05-security.md` |
| Local models | `docs/06-local-models.md` |
| MCP / plugins / connectors | `docs/07-mcp-plugins.md` |
| The build process | `docs/08-workflow.md` |
| Build + release | `docs/09-build-and-release.md` |
| Definition of done | `docs/10-acceptance.md` |
| Settled open questions | `docs/11-tbc-resolutions.md` |
| Terms, explained in German | `docs/glossary-de.md` |
