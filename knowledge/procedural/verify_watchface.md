---
generated_by: "OpenAI Codex (GPT-6; exact variant not exposed)"
timestamp: "2026-11-07T08:28:18-06:00"
---

# Verify Loose Digits

Production: `python3 execution/build.py`, then `python3 execution/verify.py`. Host tests use ASan/UBSan; production ELF symbols must exclude the fixture-only clock/pose variables. Build output goes to dist; temporary test binaries and evidence stay in .tmp.

Native evidence, one emulator owner at a time:

1. Run `python3 execution/build.py --fixture`.
2. Install `.tmp/Loose-Digits-fixture.pbw` with `pebble install --emulator emery`.
3. Run `python3 execution/capture_native.py --platform emery`.
4. Run `python3 execution/check_sensor.py --platform emery`.
5. Stop the owned emulator with `pebble kill` before switching targets.
6. Repeat for chalk, then gabbro.
7. Finish with a production build and verification.

Do not use pkill -9. Do not inspect waf lock files or print pypkjs process arguments: they can contain credentials. Capture tooling only parses QEMU arguments in memory to obtain its monitor port.

Frozen poses in native-motion.gif are renderer evidence, not live sensor evidence. sensor-motion.gif captures the real sensor-triggered animation at sampled framebuffer times. Screen-dump palette normalization restores the known full-scale 64-color levels; raw PPM files are discarded. The fixture sets sample date to 2026-11-07 and time to 10:42, independent of production time.

Live sensor check injects neutral acceleration then a constant rolled vector. It checks visible motion, exact final rest, no repeated animation while held rolled, Motion Off, and a minute change during motion. Native settings messages exercise on-watch persistence; real companion Save/Cancel remains a physical-phone test.

## 2026-11-07 learnings

If installation reports success but the wrong face remains active, do not collect evidence. Dismiss any old not-responding dialog with Back; hold Select to open the menu; open Watchfaces; select Loose Digits explicitly. Reinstalling alone did not resolve this Gabbro session. Capture guards reject wrong background or unchanged sample time/motion. A fresh visual reviewer caught the original incorrect Gabbro captures; they were replaced after activation.

## 0.2.0 knock/color acceptance

After fixture install and active-version confirmation, run `python3 execution/check_knocks_colors.py --platform emery`; repeat for chalk/gabbro with exclusive emulator ownership. This injects synthetic top-axis knocks, verifies mode0 single rejection, double trigger/return, mode1 single trigger, Motion Off, custom palette colors, reinstall persistence, and dark/bright-green contrast fallback. Color probe rejects an old version of the same face still active after install. Host knock tests also cover X and Z axes, rebound, timeout, cooldown and timestamp wrap. No physical detection claim follows from these fixtures.

Build filenames derive from package.json version, avoiding manual release-path drift. Preserve prior dist files as local previous versions.

Reinstall persistence checks poll for the expected framebuffer for up to five seconds; a fixed half-second capture caught a transient Chalk redraw. Round2 intermittently missed a 20ms synthetic input despite valid timestamp telemetry on passing trials; the final fixture holds each peak for two samples. This does not establish real-case detection sensitivity.
