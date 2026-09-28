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

### Notes
- No application code exists yet. Implementation begins at `plan/phase-00-foundation/T-001`.
