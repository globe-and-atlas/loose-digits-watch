---
generated_by: "OpenAI Codex (GPT-6; exact variant not exposed)"
timestamp: "2026-11-07T08:28:18-06:00"
---

# Decisions — 2026-11-07

- Use one native C watchface for Emery, Chalk, Gabbro. No phone network service is necessary for time or motion.
- Separate pure gesture/pose/time policy from Pebble service wiring to exercise failure-prone cases on the host.
- Require neutral arming and two rolled samples; use a five-second trigger cooldown. Reject gestures during the finite three-second animation. A tap-only trigger was rejected because the approved concept is a wrist roll.
- Use 25 Hz acceleration in batches of five. No redraw timer runs at rest; animation draws at up to 20 Hz. Energy impact remains unmeasured.
- Draw original 5×7 digits directly. Inverse-map rotated whole glyphs into horizontal pixel runs to avoid per-cell polygon antialias seams. No per-frame heap allocation.
- Native default is pale yellow (#FFFFAA), a real Pebble palette color, rather than promising the off-palette cream of the concept art.
- Date defaults Off; expose ISO, US, EU options per Pebble workspace convention.
- Do not publish or claim sharing performance from this build.

## 2026-11-07 — 0.2.0 input and color revision

- Double case knock is now the default. Single knock and original wrist roll remain selectable; existing Motion Off remains respected. SDK touchscreen is intentionally restricted to watchapps according to the current official touch guide, so do not imply capacitive touch support.
- Raw acceleration is sampled at 50 Hz in batches of five (0.1.0 used 25 Hz). Peak deltas of 700 mg on any axis constitute impact candidates; reject candidates within 120 ms as rebound, pair candidates within 650 ms. Raw timestamps preserve within-batch event timing. Impacts during animation cannot restart its timer. Physical success/false-trigger rate remains unknown.
- Independent background, digit/date, and colon RGB settings use appended message keys and persisted IDs 4–6. UUID and old message key order are preserved. Trigger is persisted at ID 3.
- Equal palette ink/background gets black or white via weighted quantized luminance; equal accent/background uses the chosen readable ink. Bright green required a weighted test because channel-sum heuristics chose low-contrast white.
