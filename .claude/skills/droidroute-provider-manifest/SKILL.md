---
name: droidroute-provider-manifest
description: Add or change a provider in DroidRoute - write the manifest, confirm the base URL from the provider's own documentation, validate with a live call, tag free tiers, and keep the docs in sync. Use for any task in plan/phase-02 or plan/phase-03, or when the user asks to add/integrate a provider or gateway.
---

# Provider work

## The one rule that matters

**Never guess a base URL, auth header, field name or model id.** A wrong URL produces a provider that silently never works — worse than a missing one. Read the provider's own documentation; if it is unreachable, stop and record the blocker in the task log.

## Manifest shape

```json
{
  "id": "example",
  "name": "Example Gateway",
  "tier": 1,
  "compat": "openai",
  "base_url": "https://.../v1",
  "auth": { "type": "bearer" },
  "models_source": { "type": "discovery", "path": "/models" },
  "fallback_models": [],
  "quota": { "window": "daily", "hint_tokens": 0 },
  "tags": ["free", "one-click"],
  "notes": "one line that is true"
}
```

Tier 1 = free/credit gateways, Tier 2 = paid majors, Tier 3 = long tail and local. Tags drive the UI filters and the `free_first` strategy.

## Checklist

1. Confirm `base_url`, auth style and the models endpoint from the provider's docs — quote the finding in the log.
2. Write the manifest; keep `fallback_models` empty unless the provider has no discovery endpoint.
3. Validate with a real key: models list first, one cheap chat call second. Record the model count and latency.
4. Tag free tiers so `free_first` can prefer them without hard-coded id lists.
5. Add the row to `docs/03-providers.md` in the same commit, then run `python3 tools/check_providers.py`.
6. If anything stays unconfirmed, mark the manifest `draft: true` and leave it disabled. Never ship a guess as if it were a fact.

## Verification

```bash
python3 tools/check_providers.py
./gradlew :app:testDebugUnitTest --tests '*<provider>*'
scripts/log-step.sh T-0xx "run" "live validation <provider>" "<result>"
```

## Custom provider path

Anything OpenAI- or Anthropic-compatible also has to work through the in-app form (T-033) with model discovery and a manual fallback. If a provider needs a special case in the adapter instead, that is a design smell: extend the manifest schema or the generic adapter, and say why in `status/DECISIONS.md`.
