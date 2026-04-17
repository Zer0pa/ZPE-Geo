# 2026-03-21 Operator Status Pack

This directory is the copied-back March 21 operator evidence pack for the Git-backed repo.

It exists so the repo can state current March 21 status locally instead of referring only to the outer workspace.

## What Is Here

| Path | Meaning |
| --- | --- |
| `phase0311_runpod/handoff_manifest.json` | supporting handoff artifact; useful but hybrid because it preserves current red-state fields alongside historical February 20 fields |
| `phase0311_runpod/max_claim_resource_map.json` | current claim split: unresolved claims versus current PASS claims |
| `phase0311_runpod/RUN_MANIFEST.json` | compact command-chain execution record |
| `phase0311_runpod/max_av2_resume_state.json` | AV2 durable continuation state as copied back |
| `phase0311_runpod/max_noaa_ais_resume_state.json` | NOAA AIS durable continuation state as copied back |
| `phase0311_runpod/GIT_FRESHNESS.json` | freshness evidence for the RunPod execution surface |
| `phase0311_runpod/RUNPOD_SYNC_RECEIPT.json` | explicit file-sync proof for the RunPod execution surface |
| `release_alignment/TECHNICAL_ALIGNMENT_REPORT.md` | copied-back package-alignment truth from the March 21 technical alignment pass |

## How To Read It

- Read [../../../README.md](../../../README.md) as the governing current verdict and release-gate summary.
- Read this pack as supporting current operator evidence, not as a standalone interpretation layer.
- Read [../../../docs/LEGAL_BOUNDARIES.md](../../../docs/LEGAL_BOUNDARIES.md) for the current-versus-historical boundary and explicit limits.
- Read [../../../docs/ARCHITECTURE.md](../../../docs/ARCHITECTURE.md) for the repo map and evidence routing.
- Read [../2026-02-20_zpe_geo_wave1/](../2026-02-20_zpe_geo_wave1/) as historical generated evidence.
