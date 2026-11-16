---
generated_by: "OpenAI Codex (GPT-6; exact variant not exposed)"
timestamp: "2026-11-07T11:43:04-06:00"
---

# Publish Loose Digits

Run only with explicit user authorization for the named store publication. The 2026-11-07 request authorizes the first0.2.0 listing for Emery, Chalk and Gabbro.

## Prepare

Use execution/prepare_store_media.py against the correct native fixture for each platform. It captures actual runtime poses and color settings, produces lossless animated/still GIFs, and checks native dimensions plus decoded frames/timing. GIF stills avoid the observed store PNG palette processing. Native emulator captures are not physical-watch evidence.

Finish with execution/build.py and execution/verify.py to generate a clean production PBW. The publish path must never rebuild it. Run tests/test_publish_store.py using the installed Pebble-tool Python environment. Run execution/publish_store.py prepare in that environment; obtain fresh independent artifact/media/copy review before the publish action.

## Publish

Execution/publish_store.py publish uploads the exact plan PBW through stored SDK authentication. It refuses changed UUID mapping, an existing receipt or an ambiguous inflight guard. POST is never retried automatically. Reconcile server state after an ambiguous result before any new write. Never print SDK tokens, pypkjs arguments, or waf lock files.

## Verify

Open the public listing and select Time2, originalTimeRound, Round2. Record rendered gallery image URLs, deduplicating the live-watch placeholder copy of the first image. Save those URLs in .tmp/store-publication/ui-galleries.json. Run execution/publish_store.py verify. Require the public PBW hash to equal the plan; require public media frames/pixels/timing to match each staged asset; require each animation to lead its gallery. Independent public review completes the evidence.

Receipts: release/store-plan.json, release/store-release.json, release/public-proof.json. Do not change unrelated listings, push Git source, or infer sharing/download performance from visible counts.
