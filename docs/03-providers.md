# Providers

A provider is **data, not code**. Each one is a JSON manifest in `assets/providers/<id>.json`, loaded at startup into the registry. Adding a provider that speaks OpenAI or Anthropic compatibility requires no Kotlin change.

## Manifest schema

```json
{
  "id": "bynara",
  "name": "Bynara / NaraRouter",
  "homepage": "https://bynara.id",
  "tier": 1,
  "compat": "openai",
  "base_url": "https://router.bynara.id/v1",
  "auth": { "type": "bearer", "env_hint": "BYNARA_API_KEY" },
  "models_source": { "type": "discovery", "path": "/models" },
  "fallback_models": ["qwen-3.8-max-free", "glm-5.3-air-free"],
  "quota": { "window": "daily", "hint_tokens": 7000000 },
  "notes": "Free tier, ~7M tokens/day, 50+ models, OpenAI-compatible.",
  "tags": ["free", "one-click", "aggregator"]
}
```

| Field | Meaning |
|---|---|
| `compat` | `openai` \| `anthropic` \| `gemini` — which decoder/encoder to reuse |
| `auth.type` | `bearer` \| `x-api-key` \| `none` \| `oauth-google` \| `oauth-github` \| `oauth-hf` \| `session` (experimental) |
| `models_source` | `discovery` (calls the provider), `static` (list in manifest), `manual` (owner types it) |
| `tier` | 1 = free/credit gateways, 2 = majors, 3 = long tail/local — drives the "free first" strategy |
| `tags` | `free`, `one-click`, `aggregator`, `local`, `media`, `embeddings` — used by the UI filters |

## Tier 1 — free and credit-heavy gateways (built first)

| Provider | Base URL | Compat | Notes |
|---|---|---|---|
| Bynara / NaraRouter | `https://router.bynara.id/v1` | openai | **Owner's priority.** Free tier, ~7M tokens/day, ~50 models |
| FreeLLMAPI | self-hosted, e.g. `http://127.0.0.1:3001/v1` | openai | Combines ~34 free provider tiers behind one key |
| APInex | `https://apinex.bond/v1` | openai | Free models with daily-reset limits |
| GoRouter | provider-supplied base | openai + anthropic | Free credits, Anthropic-style endpoints offered |
| TokenRouter | provider-supplied base | openai | Credit gateway, discovered at runtime via `models_source` |
| TokenReply | provider-supplied base | openai | Credit gateway, same treatment |
| FastRouter | provider-supplied base | openai | Latency-oriented router front-end |
| xKiro | `https://api.xkiro.com/v1` | openai | "Every leading model, one API key" |
| Experiential Labs | `https://api.experientiallabs.ai/v1` | openai | Zero-markup gateway; can also front the owner's own keys |
| OpenRouter | `https://openrouter.ai/api/v1` | openai | Free model subset tagged `free` |
| Groq | `https://api.groq.com/openai/v1` | openai | Free tier, very low latency |
| Cerebras | `https://api.cerebras.ai/v1` | openai | Free tier, high throughput |
| Google AI Studio | `https://generativelanguage.googleapis.com/v1beta` | gemini | Free tier key, separate from the AI Pro OAuth account |
| Mistral | `https://api.mistral.ai/v1` | openai | Free experimental tier |
| GitHub Models | `https://models.inference.ai.azure.com` | openai | Free with a GitHub token |
| Cloudflare Workers AI | `https://api.cloudflare.com/client/v4/accounts/{id}/ai/v1` | openai | Free daily neurons |
| NVIDIA NIM | `https://integrate.api.nvidia.com/v1` | openai | Generous free credits |

> Base URLs marked "provider-supplied" are resolved during the implementation task by reading the provider's own documentation; the manifest carries a `discovery_task` field pointing at the task file that fills it in. No invented URLs are ever committed — a wrong URL is worse than an empty one.

## Tier 2 — majors, keys and subscriptions

OpenAI, Anthropic, Google Gemini (AI Pro **OAuth**), Perplexity (**Sonar**, see `docs/11-tbc-resolutions.md` TBC-5), xAI, DeepSeek, Alibaba DashScope/Qwen, Together, Fireworks, DeepInfra, Novita, Hyperbolic, Nebius, SambaNova, Cohere, AI21, HuggingFace (OAuth + Inference API), Scaleway, Chutes, Kluster.

## Tier 3 — long tail and local

Anything OpenAI- or Anthropic-compatible the owner adds through the provider form, plus local runtimes: llama.cpp in Termux (`local/llamacpp`), an optional Ollama or LM Studio endpoint on the LAN, and the embedded runtime once it ships.

## One-click connect

Providers tagged `one-click` get a **Connect** button that:

1. opens the provider's key page in the browser (`homepage` + `key_path` from the manifest),
2. returns via deep link,
3. prompts for the key, validates it with a single cheap call (`models_source.path`),
4. stores it in the vault, shows the masked key, and marks the provider enabled.

Free providers are always tried first, so a `one-click` provider that fails validation is never silently enabled.

## Key handling rules

- Keys are stored per `(provider, label)` — multiple keys per provider are normal, not a special case.
- A key is revealed in plaintext **exactly once** (at entry or on explicit "reveal" with device-credential confirmation); afterwards the UI shows `first5••••last5`.
- Validation calls are logged but never store the response body (it may echo the key).
- A key that returns `401` is marked `invalid` and taken out of rotation without being deleted.
- Deleting a provider deletes its keys from the vault in the same transaction.

## Custom providers

The form accepts: display name, base URL, compat (`openai` | `anthropic`), auth type, optional default headers, optional model list, and a "discover models" button. Discovery failure falls back to a manually typed list — never to a guess. Custom providers can be exported as a manifest file (without secrets) so they can be shared or re-imported.
