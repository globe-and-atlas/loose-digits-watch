---
generated_by: "OpenAI Codex (GPT-6; exact variant not exposed)"
timestamp: "2026-11-07T08:28:18-06:00"
---

# Loose Digits — implementation

## Contract
- Directive: `directives/build_watchface.md`.
- Execution: `execution/build.py`, `execution/verify.py`, `execution/capture_native.py`.
- Artifact: `dist/Loose-Digits-0.1.0.pbw`.
- Boundaries: local build only; no publication, push, physical-watch installation, or secret reads.

## Validation contract
- [x] PBW contains an Emery binary.
- [x] PBW contains a Chalk binary.
- [x] PBW contains a Gabbro binary.
- [x] Resting digits fit within Emery's screen.
- [x] Resting digits fit within Chalk's circle.
- [x] Resting digits fit within Gabbro's circle.
- [x] A deliberate roll from neutral triggers a tumble.
- [x] Constant neutral samples do not trigger a tumble.
- [x] Constant rolled samples do not retrigger a tumble.
- [x] Motion finishes within 3200 ms without additional input.
- [x] Repeated gestures cannot postpone reassembly.
- [x] The clock returns to exact resting geometry.
- [x] Minute changes during animation show current time after reassembly.
- [x] Motion Off prevents gesture animations.
- [x] Date Off hides the date.
- [x] ISO date renders YYYY-MM-DD.
- [x] US date renders MM/DD/YYYY.
- [x] EU date renders DD/MM/YYYY.
- [x] Watch 12-hour preference is honored.
- [x] Watch 24-hour preference is honored.
- [x] Production contains no fixture overrides.
- [x] Host behavior tests pass.
- [x] Native Emery renders are inspected.
- [x] Native Chalk renders are inspected.
- [x] Native Gabbro renders are inspected.
- [x] Fresh independent review passes.

## Implementation
- [x] Scaffold project with canonical script.
- [x] Implement native face.
- [x] Run verification.
- [x] Record final handoff.

## Verification result

2026-11-07: sanitizer host tests, settings lifecycle tests, native render review, live emulator sensor tests passed. Independent creator-verifier PASS. Production SHA-256: `1b38304a9c2c6dadb062cef34e6050b37a92bff78aaa346501c3341dea96e4b7`.

Physical-watch acceptance and 30-day voluntary sharing are outside this local implementation contract.

## 0.2.0 — knock triggers and colors

Artifact: `dist/Loose-Digits-0.2.0.pbw`. Local build only.

- [x] Two case-knock impulses within 650 ms trigger motion by default.
- [x] One knock does not trigger double-knock mode.
- [x] One knock triggers single-knock mode.
- [x] Rebound within 120 ms cannot count as the second knock.
- [x] Knock handling ignores the accelerometer axis.
- [x] Wrist roll remains selectable.
- [x] Motion Off prevents knock-triggered animation.
- [x] Knock animation reassembles automatically.
- [x] Background color persists after reinstall.
- [x] Digit color persists after reinstall.
- [x] Accent color persists after reinstall.
- [x] Native custom colors render on Emery.
- [x] Native custom colors render on Chalk.
- [x] Native custom colors render on Gabbro.
- [x] Current touchscreen restriction is described accurately.
- [x] Updated host tests pass.
- [x] Clean production three-target build passes.
- [x] Independent review passes.

0.2.0 verified: host sanitizer/settings tests, three-target native knock/color/persistence checks, clean production bundle, independent review PASS. Physical sensitivity remains unverified.

## Store publication — authorized 2026-11-07

The user explicitly authorized publishing Loose Digits0.2.0 with native screenshots and animated previews. This supersedes local-only boundaries for this release. No Git push or unrelated listing change is authorized.

- [x] Emery gallery contains a native tumble/color GIF.
- [x] Chalk gallery contains a native tumble/color GIF.
- [x] Gabbro gallery contains a native tumble/color GIF.
- [x] Emery gallery contains native still screenshots.
- [x] Chalk gallery contains native still screenshots.
- [x] Gabbro gallery contains native still screenshots.
- [x] Listing explains case-knock triggering.
- [x] Listing distinguishes preview color changes from installed behavior.
- [x] Final production bundle passes verification.
- [x] Independent release review passes.
- [x] Publication uses the reviewed PBW bytes.
- [x] Public PBW hash matches the submitted artifact.
- [x] Public Emery media match staged pixels.
- [x] Public Chalk media match staged pixels.
- [x] Public Gabbro media match staged pixels.
- [x] Public version is0.2.0.

Published2026-11-07: public0.2.0 PBW hash and12gallery asset bytes/pixels/timing verified; independent public review PASS.
