# Component: competitive-edge

**Purpose:** absorb what the other routers do well, refuse what conflicts with the owner's rules, and build the capabilities that only exist because this gateway runs on a phone.

| | |
|---|---|
| State | ⬜ not started |
| Tasks | T-167 … T-184 |
| Owns | provider auto-detection, migration importers, local-first providers, extra wire surfaces, subscription login, tool-output compression, response-style presets, conversation affinity, offline mode, device-state routing, Android surfaces, mobile-data budget, offline model catalog, self-update, signed catalog packs, debug capture, QR config transfer, the native benchmark |
| Depends on | provider-layer, protocols, routing, core-server, delivery |

## Deliverables

- Any endpoint becomes a provider by pasting a URL and confirming the inferred manifest (T-167).
- Configs from OmniRoute, 9Router, LiteLLM, one-api/new-api and CLIProxyAPI import with a report (T-168).
- A configured local provider never falls back to a cloud host, and no-auth providers connect without a key (T-169).
- The OpenAI Responses shape and Vertex AI with ADC work as providers and as client surfaces (T-170).
- CLI-subscription identities log in, and several accounts per provider rotate on the same quota ledger as keys (T-171).
- Tool output — `git diff`, `grep`, logs — is compressed losslessly with a bypass header (T-172).
- Brevity presets exist, default off, and never override an explicit instruction (T-173).
- A conversation stays on one provider while it is healthy, so prompt caches survive (T-174).
- With no connectivity, a loaded local model answers and cloud-only work is queued and replayable (T-175).
- Battery, thermal and metered-connection policies produce explainable routing decisions (T-176).
- Quick Settings tile, widget, share sheet and text-selection action all work without opening the app (T-177).
- Mobile-data usage is counted per provider and network type, with an optional hard stop (T-178).
- The model catalog works in airplane mode and a tampered update pack is rejected (T-179).
- The app detects a newer release, verifies the APK signature, installs, and can roll back (T-180).
- Provider and model knowledge updates as a signed pack, without an app release (T-181).
- Debug capture is redacted, time-bounded and auto-expiring (T-182).
- A configuration moves to a new phone by QR code, encrypted, with no cloud involved (T-183).
- The native-versus-Node claim is backed by measured numbers, or corrected in public (T-184).

## Open risks

- T-171 and T-184 depend on external software and real subscriptions: each may end as a documented "not feasible, here is the evidence" rather than a working adapter. That is an accepted outcome, not a failure — but no adapter may be claimed as working without a recorded run.
- T-180 installs an APK from the network. Signature verification against the pinned certificate is the control that makes this safe; without it the feature must stay off.
- T-176's thermal and battery policies change behaviour based on device state, which makes bugs state-dependent. The reason string on every decision is the debugging handle.
- Ordering: phase 13 depends on delivery (T-136…T-147), so it cannot start before v0.1 is closed.

## Evidence log

_No entries yet._
