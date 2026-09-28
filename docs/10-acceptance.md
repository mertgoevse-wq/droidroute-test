# Acceptance Criteria

The chain is done when all sixteen are met. Each one names how it is proven — a criterion without a command or a concrete observation is not accepted.

| # | Criterion | How it is proven |
|---|---|---|
| A1 | App runs on the Galaxy A56; server starts with a persistent notification; port is configurable | Install the CI APK, change the port in Settings, confirm with `curl http://127.0.0.1:<port>/health` from Termux |
| A2 | Claude Code and Freebuff work through localhost with no extra configuration | `ANTHROPIC_BASE_URL` / `OPENAI_BASE_URL` exported, one real prompt each, response returned, entry visible in the dashboard |
| A3 | Provider coverage: all Tier 1 providers plus the owner's named extras are selectable; custom providers can be added by form; at least one free provider connects one-click | Provider list screenshot + a successful call per provider that the owner holds credentials for; one provider added by hand from a form |
| A4 | Google AI Pro (OAuth) and Perplexity (Sonar) are connected; Perplexity returns citations | `POST /v1/search` returns `answer` + non-empty `citations[]`; Google provider answers a prompt through the OAuth account |
| A5 | Failover and key rotation demonstrably work | Inject a `401`/`429` (temporary invalid key or exhausted quota) → request still succeeds via the next key/provider; `/v1/routing/explain` and the attempt list in logs agree |
| A6 | Dashboard shows tokens per provider, daily/weekly usage, errors, latency | Values compared against `/v1/usage` JSON for the same window |
| A7 | A local model runs via Termux, started and stopped from the app, with a memory warning | Load a ≤4 GB `.gguf`, get a completion through `local/llamacpp/...`; the warning appears for an oversized model |
| A8 | MCP servers from Termux/Debian are discovered automatically, manually addable, and all enabled ones are offered to agents | `GET /mcp/servers` matches `~/.claude.json`; a `tools/call` through `POST /mcp/{id}` returns a real tool result |
| A9 | Repository is private; an autonomous run produced ≥135 task files and built the project from them; every step committed and pushed | `gh repo view --json isPrivate`; `ls plan/**/T-*.md | wc -l` ≥ 135; `git log --oneline` shows one commit per task; `git status` clean |
| A10 | A different model or program can take over from the repository alone | Fresh session with no chat history: read `status/` and complete one task end to end |
| A11 | APK builds automatically on GitHub and is installable; the Termux fallback is documented and tested once | Green workflow run + installed artifact; a local `assembleDebug` run recorded in `logs/` |
| A12 | Repository hygiene: no secrets, logs pruned weekly, README accurate | `scripts/preflight-secrets.sh` clean; cleanup workflow ran at least once; README links all resolve |
| A13 | Build agents can see and use every available skill, plugin and MCP server | `python3 scripts/discover_tooling.py --check` passes in CI and `--check-fresh` passes on the device; `status/TOOLING.md` lists the real installed skills/plugins/MCP servers; every phase in `handbooks/03-skills-catalog.md` names skills that exist in that inventory; `python3 tools/check_skills.py` passes, proving every role label a task names resolves to an installed tool; a task log shows a skill substitution recorded |
| A14 | An unknown provider can be added by pasting a URL, and a rival router's configuration can be imported | T-167 detects each of the four stub dialects and refuses to enable a provider whose probe returned nothing; T-168 imports each fixture format, with any credential found moved to the vault rather than into a manifest |
| A16 | The interface is the decided instrument panel of `docs/14-design-system.md` — not a generated dashboard — and that is provable | `python3 tools/check_design_slop.py` clean on the real tree **and** `--self-test` passing (a gate that no longer bites is a failure); T-186's proof table shows every rule failing on an injected violation and reverting clean; T-185 records zero token drift; T-188 records the measured contrast ratio of every used pair in both modes against its threshold; T-187 supplies both-mode screenshots per screen with a named focal element and a closed finding list; T-189 shows all five states per data screen; T-190 lists the residual weaknesses without softening them |
| A15 | The app behaves like an Android app and stays current without the owner re-installing it by hand | T-177 tile/widget/share sheet work on the device and the widget produces no periodic wakeups; T-175 answers a request with connectivity off and a local model loaded; T-176 refuses metered traffic under policy and names the reason; T-180 detects a newer release, verifies its signature, and refuses one that does not match; T-181 applies a signed catalog pack without an app update and rejects a tampered one |

## Regression gate

Every task's verification commands are the gate. A task that breaks a previously passing check is not complete, even if its own criteria pass — the failure goes to `status/ERRORS.md` and the task is repaired before the chain advances.

## Evidence trail

For A1–A16, evidence is: the task log line, the verification command, and its raw output stored under `logs/tasks/`. Screenshots are attached to the task file only when the proof is visual (A3, A7).
