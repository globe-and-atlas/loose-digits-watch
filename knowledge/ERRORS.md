---
generated_by: "OpenAI Codex (GPT-6; exact variant not exposed)"
timestamp: "2026-11-07T08:28:18-06:00"
---

# Reproducible findings — 2026-11-07

## Rotating independent pixel cells creates seams

Error: native tilted digits appeared broken into speckles despite valid rotated cell bounds.
Cause: antialiasing each small filled polygon independently creates repeated light seams at cell boundaries.
Fix: inverse-map a whole glyph into contiguous horizontal native-pixel runs, preserving the resting bit pattern without per-cell polygon edges.
Graduated-to: `knowledge/DECISIONS.md`, native renderer in `watchface/src/c/main.c`.

## Successful install can leave another watchface active

Error: Gabbro dimension-only captures were initially labeled PASS while showing the old PBL-2500 face; sensor assertions consequently failed.
Cause: install success established bundle transfer, not active-face identity. Emulator retained another face and then its not-responding dialog.
Fix: dismiss the dialog, hold Select, open Watchfaces, explicitly select Loose Digits. Confirm face identity before gathering evidence. Capture script now checks the known background and rejects identical rest/tumble or rest/late states. Independent visual review remains required.
Graduated-to: `knowledge/procedural/verify_watchface.md`.

## Equal-color fallback on bright green

Error: a channel-sum fallback picked white ink when foreground and background both quantized to bright green. Cause: green contributes disproportionately to perceived luminance. Fix: weighted RGB luminance selects black; sanitizer host regression and native green cases verify it. Graduated-to: DECISIONS.md, ld_background_is_light.
