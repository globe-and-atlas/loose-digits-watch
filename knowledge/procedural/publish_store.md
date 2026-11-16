---
generated_by: "OpenAI Codex (GPT-6; exact variant not exposed)"
timestamp: "2026-11-07T11:43:04-06:00"
---

# Store publication — 2026-11-07

User explicitly authorized first publication of Loose Digits0.2.0 for three native targets with screenshots and tumble/color animation. See directives/publish_watchface.md and execution/publish_store.py for the reproducible flow.

The publisher reuses workspace execution/publish_watchface_updates.py for SDK account mapping, allowed public download hosts, bounded GET retries, and atomic JSON writes. Six focused tests exercise existing-receipt skip, inflight guard, changed UUID mapping, POST timeout, rejection, successful receipt. Mutating requests are never retried blindly.

Screenshots are captured by native fixture renderer and uploaded as lossless GIFs: one motion/color animation plus three still GIFs per target. The lead loop is11,050ms and returns to identical resting pixels. Color examples represent settings choices, not automatic color cycling. Existing physical knock/battery gaps remain in store description.

Public UI may insert a live-watch preview that duplicates the first gallery source and shifts Screenshot alt numbering. Collect all Screenshot image src values for the selected platform and deduplicate them while preserving order. Do not assume alt1–4 are the four actual media assets. Native public proof compares every decoded frame, timing, and artifact hash after observed gallery selection.

Public URL: https://apps.repebble.com/391620b25cbf4bf39565ab49 . No unrelated listing or Git push was changed.
