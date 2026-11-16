---
generated_by: "OpenAI Codex (GPT-6; exact variant not exposed)"
timestamp: "2026-11-07T08:28:18-06:00"
---

# Loose Digits

[Get Loose Digits0.2.0 on the Pebble store](https://apps.repebble.com/391620b25cbf4bf39565ab49). Native galleries cover Time2, originalTimeRound, Round2.

A native Pebble watchface for Time 2 (Emery 200×228), original Time Round (Chalk 180×180), and Round 2 (Gabbro 260×260).

Large original pixel digits rest on a light yellow 64-color background with a coral colon. Two quick knocks on the case make the digits tumble. Single case knock and wrist roll are selectable alternatives. They reassemble automatically after three seconds. Time follows the watch's 12/24-hour preference. Single-digit 12-hour times are centered; AM/PM remains visible. Date is Off by default.

## Use

Install `dist/Loose-Digits-0.2.0.pbw` through the Pebble companion app. Use two quick case knocks within 650 ms by default. A 120 ms rebound filter prevents a single impulse and its return from being treated as two knocks. The detector uses acceleration changes along any axis; it cannot identify the physical side struck. A five-second cooldown begins at the trigger; further movement cannot extend the animation. Wrist-roll mode requires briefly holding the watch approximately face-up before rolling sideways. Phone settings offer Animation On/Off, Double case knock / Single case knock / Wrist roll, and independent Background, Digits & date, Colon accent color pickers. Colors are quantized to the Pebble palette and persist on the watch. If ink matches the background after quantization, a black/white contrast fallback keeps the time readable. Choose Date Off, YYYY-MM-DD, MM/DD/YYYY, or DD/MM/YYYY.

## Build and verify

Requires Pebble Tool 5.0.40, SDK 4.33.1, Node/npm, a host C compiler, Python 3, and Pillow for native evidence collection. Run:

```sh
cd watchface
npm ci --ignore-scripts
cd ..
python3 execution/build.py
python3 execution/verify.py
```

The build clears LD_* environment flags before a clean compile. `--fixture` writes only `.tmp/Loose-Digits-fixture.pbw`; it never overwrites dist. Native evidence collection is in `knowledge/procedural/verify_watchface.md`.

## Screen touch

Current Pebble touch input is restricted to watchapps, not watchfaces: [official guide](https://developer.repebble.com/guides/events-and-services/touch/). This face uses physical case-knock acceleration, not capacitive screen touch. A light screen contact that produces no detectable impulse will not trigger it.

## Evidence boundary

Version0.2.0 is publicly listed. The public PBW and native galleries have a separate release proof in release/public-proof.json. Automated host behavior checks and native emulator sensor tests do not establish physical gesture comfort, false-trigger rate, endurance, real companion settings behavior, or voluntary sharing. The animation deliberately makes time harder to read briefly; Motion Off provides a still clock.
