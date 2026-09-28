---
name: droidroute-compose-ui
description: Build DroidRoute's Compose UI - screens for dashboard, providers, keys, routing, settings and logs - using the installed Android and design skills, with German-first strings and honest state displays. Use for plan/phase-07 tasks, or when the user asks for a screen, layout, visual polish or a design review of the app.
---

# UI work

## Pair this skill with a real Android or design skill

Check `status/TOOLING.md` for what is installed. Good pairings for this project:

| Need | Skills |
|---|---|
| Material 3 structure, adaptive layouts | `mobile-android-design`, `adaptive`, `edge-to-edge` |
| Visual polish and hierarchy | `impeccable`, `craft`, `polish`, `typeset`, `layout` |
| Accessibility | `accessibility`, `web-design-guidelines` (structural rules transfer) |
| Performance of lists and recomposition | `optimize`, `android-profiler` |
| Motion | `animate`, `vercel-react-view-transitions` (concepts only) |

Never ship a screen without a second opinion from at least one of these.

## Project rules that override generic advice

1. **German is the default resource set**, English is `values-en/`. No user-facing string literal in a composable — the lint check enforces it.
2. **Never show a secret outside the keys screen.** Keys are `first5••••last5`; reveal needs device-credential confirmation; `FLAG_SECURE` on those screens only.
3. **Colour is never the only signal** for provider health — pair it with a label or shape.
4. **Honest states:** an empty dashboard names the next action instead of showing zeros; a failed provider names the failure instead of a red dot; an unknown price is labelled unknown, never estimated silently.
5. **Numbers come from the API** (`/v1/usage`, `/v1/providers`, `/v1/routing/explain`) — no UI-side re-derivation of values that already exist.

## Verification for UI tasks

```bash
./gradlew :app:assembleDebug
./gradlew :app:lintDebug
```

Then, for anything visual, capture a screenshot or run the accessibility audit skill. "It looks fine" is not evidence; a screenshot or an audit result is.

## Accessibility floor

Touch targets at the documented minimum, content descriptions on every interactive element, no truncation at 200 % font scale, and a screen-reader pass on the screens you touched.
