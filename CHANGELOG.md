# Changelog

All notable changes to DroidRoute. Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/); versions follow [Semantic Versioning](https://semver.org/).

## [Unreleased]

### Added
- Master specification (`docs/droidroute-spec.md`) capturing the full requirements interview.
- Resolutions for every open point — port 8787, Tailscale/Cloudflare access, SDK matrix, MCP federation, Perplexity Sonar tiers, llama.cpp runtime resolution, provider tiers, build-agent tooling discovery, the scope of the parity claim, and the comparison to other routers (`docs/11-tbc-resolutions.md`).
- Repository scaffolding: `docs/`, `handbooks/`, `plan/`, `status/`, `logs/`, `scripts/`, `tools/`, `.github/`.
- Build plan (`plan/`) generated from `tools/plan_data/`: foundation, core server, provider framework and catalog, accounts/OAuth, wire protocols, routing, UI, local models, MCP, logging/handover, delivery, OmniRoute parity and the competitive-edge phase.
- Agent operating rules (`AGENTS.md`, `CLAUDE.md`) and handbooks for subagent orchestration, git protocol, logging, resume and anti-slop.
- CI: `build-apk` (debug on push, signed release on tag) and `repo-hygiene` (weekly log rotation, link and secret checks).
- Scripts: `step-commit.sh`, `log-step.sh`, `preflight-secrets.sh`, `weekly-cleanup.sh`, `termux-setup.sh`, `build-apk-local.sh`.
- **Build-agent tooling layer**: `scripts/discover_tooling.py` scans global and project scope for skills, plugins, marketplaces, slash commands and MCP servers and publishes `status/TOOLING.md` + `status/tooling.json`. CI validates the inventory's structure (`--check`); freshness is checked on the device with `--check-fresh`, because a CI runner has no agent configuration. Acceptance criterion A13 covers both.
- Six project skills (`.claude/skills/`): task runner, verification, provider manifest, routing, Compose UI, skill scout.
- Four project subagents (`.claude/agents/`): implementer, verifier, chronicler, tooling-scout.
- Project settings (`.claude/settings.json`) allowing the project scripts and auto-enabling project MCP servers; `.mcp.json.example` as the server template.
- `handbooks/08-tooling-discovery.md` defines discovery levels and precedence; `handbooks/03-skills-catalog.md` rewritten against the installed libraries with a per-phase skill matrix.
- **OmniRoute parity matrix** (`docs/12-omniroute-parity.md`, 51 capability rows plus the owner's extras) and phase 12 of the plan (T-148…T-166): combos and virtual auto models, the full 19-strategy set, fusion/pipeline, multi-factor auto scoring, adaptive admission with rolling leases, token compression, prompt-cache pinning, cost telemetry and per-key USD budgets, quota-share, opt-in memory, prompt-injection guard, credential masking, modality bridge, OCR and audio translation, video generation, A2A server, canonical model ordering with a free-tier view, CLI setup helpers with scoped tokens, and the tooling wiring task.

- **Competitive landscape** (`docs/13-competitive-landscape.md`): what 9Router, OmniRoute, CLIProxyAPI, LiteLLM, the hosted aggregators and the enterprise gateways actually offer, which capabilities are absorbed into tasks, which are refused (cloud config sync, MITM TLS interception, prompt styles applied without consent) and where DroidRoute is genuinely different because it runs on a phone.
- Phase 13 of the plan (T-167…T-184, the v0.3 milestone) delivers that absorption and the Android-only edge: provider detection from a pasted URL, migration importers, local-first providers with no cloud fallback, the OpenAI Responses and Vertex AI surfaces, CLI-subscription login with multi-account pools, lossless tool-output filters, opt-in brevity presets, conversation affinity, offline-first mode, battery/thermal/metered-aware routing, Quick Settings tile and widget, mobile-data budgeting, an offline model catalog, self-update with signature verification and rollback, signed catalog packs, redacted debug capture, QR config transfer and a measured native-versus-Node benchmark.
- Real resolutions for the remaining open points (`docs/11-tbc-resolutions.md` TBC-8…TBC-10): tooling discovery, the scope of the parity claim, and how far the comparison to other routers goes.
- `handbooks/09-skill-resolution.md` maps every role label a task names to the installed skills, plugins and MCP servers, and `tools/check_skills.py` fails the build when a label has no row or a row points at something that is not installed.
- `tools/check_links.py` replaces the inline link walker in CI; `tools/generate_plan.py --check` now runs there too.
- **Design system** (`docs/14-design-system.md`): an audit of the design guidance that existed before it (ten findings, D1–D10), then a decided direction — graphite instrument panel, one brass accent, real status lamps, borders-only depth — with OKLCH tokens, a type/space/shape scale, motion and state rules, a measured accessibility floor and the honest statement that Material You dynamic colour would have made the app's identity the owner's wallpaper (it is now opt-in, default off).
- **Design gate** (`tools/check_design_slop.py`): fails the build on glass, blur, gradients, decorative shadow, hardcoded colours, off-scale spacing, untranslated text and screens that never name loading/empty/error. `--self-test` proves the gate still bites, so a gate that has silently stopped matching is itself a failure. Wired into CI.
- **Anti-slop rules extended** (`handbooks/07-anti-slop-rules.md` §11–§14): banned aesthetics, unmanaged visual values, missing states, unearned motion — with the craft self-check added for UI diffs.
- **Phase 14 of the plan** (T-185…T-190, the v0.3 craft milestone): token conformance audit, proof that the gate fires on the real tree, screen-by-screen craft review with the four tests, measured contrast and accessibility evidence, state completeness, and design acceptance. Acceptance criterion **A16** covers it.
- **Kick-off file** (`KICKOFF.md`): one code word hands the entire build to an agent, with the rules it may not break, how to watch progress and how to resume at any point.
- **Consistency audit** (`tools/check_plan_consistency.py`): composes the other checkers and adds the invariants nothing else owned — unique ids, backwards-only dependencies, no empty task, every `T-0xx` referenced in a document exists, and every stated task count matches reality (the drift that survived two phase additions). It is what found the stale counts fixed in this release.
- `docs/12`, `README`, `AGENTS.md`, `CLAUDE.md`, `status/` and `tools/README.md` corrected to the real plan size, and every task file now carries a *Read first*, *Design contract* (UI phases), *Definition of done*, *Rules that always apply* and *Stop conditions* section.

### Notes
- No application code exists yet. Implementation begins at `plan/phase-00-foundation/T-001`.
- Plan size is 190 tasks in 15 phases; phase 11 closes the v0.1 milestone, phase 12 the v0.2 parity milestone, phase 13 the v0.3 competitive-edge milestone and phase 14 the design audit that closes the craft claim.
