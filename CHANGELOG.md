# Changelog

All notable changes to DroidRoute. Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/); versions follow [Semantic Versioning](https://semver.org/).

## [Unreleased]

### Added
- Master specification (`docs/droidroute-spec.md`) capturing the full requirements interview.
- Resolutions for all seven open points — port 8787, Tailscale/Cloudflare access, SDK matrix, MCP federation, Perplexity Sonar tiers, llama.cpp runtime resolution, provider tiers (`docs/11-tbc-resolutions.md`).
- Repository scaffolding: `docs/`, `handbooks/`, `plan/`, `status/`, `logs/`, `scripts/`, `tools/`, `.github/`.
- 147-task build plan (`plan/`) generated from `tools/plan_data/`, covering foundation, core server, provider framework and catalog, accounts/OAuth, wire protocols, routing, UI, local models, MCP, logging/handover and delivery.
- Agent operating rules (`AGENTS.md`, `CLAUDE.md`) and handbooks for subagent orchestration, git protocol, logging, resume and anti-slop.
- CI: `build-apk` (debug on push, signed release on tag) and `repo-hygiene` (weekly log rotation, link and secret checks).
- Scripts: `step-commit.sh`, `log-step.sh`, `preflight-secrets.sh`, `weekly-cleanup.sh`, `termux-setup.sh`, `build-apk-local.sh`.
- **Build-agent tooling layer**: `scripts/discover_tooling.py` scans global and project scope for skills, plugins, marketplaces, slash commands and MCP servers and publishes `status/TOOLING.md` + `status/tooling.json`. CI validates the inventory's structure (`--check`); freshness is checked on the device with `--check-fresh`, because a CI runner has no agent configuration. Acceptance criterion A13 covers both.
- Six project skills (`.claude/skills/`): task runner, verification, provider manifest, routing, Compose UI, skill scout.
- Four project subagents (`.claude/agents/`): implementer, verifier, chronicler, tooling-scout.
- Project settings (`.claude/settings.json`) allowing the project scripts and auto-enabling project MCP servers; `.mcp.json.example` as the server template.
- `handbooks/08-tooling-discovery.md` defines discovery levels and precedence; `handbooks/03-skills-catalog.md` rewritten against the installed libraries with a per-phase skill matrix.
- **OmniRoute parity matrix** (`docs/12-omniroute-parity.md`, 51 capability rows plus the owner's extras) and phase 12 of the plan (T-148…T-166): combos and virtual auto models, the full 19-strategy set, fusion/pipeline, multi-factor auto scoring, adaptive admission with rolling leases, token compression, prompt-cache pinning, cost telemetry and per-key USD budgets, quota-share, opt-in memory, prompt-injection guard, credential masking, modality bridge, OCR and audio translation, video generation, A2A server, canonical model ordering with a free-tier view, CLI setup helpers with scoped tokens, and the tooling wiring task.

### Notes
- No application code exists yet. Implementation begins at `plan/phase-00-foundation/T-001`.
- Plan size is now 166 tasks in 13 phases; phase 11 closes the v0.1 milestone and phase 12 delivers the v0.2 parity milestone.
