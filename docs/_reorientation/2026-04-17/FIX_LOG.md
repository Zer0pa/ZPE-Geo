# Reorientation Fix Log -- 2026-04-17

## Drift

- [`README.md:17-21`](../../../README.md) -- replaced the dead local-asset nav strip with live text links so the front-door routing works in the current repo state.
- [`README.md:214-221`](../../../README.md) -- renamed the `Go Next` routes to match the docs that still exist in this repo and removed dead reader-routing labels.
- [`CHANGELOG.md:16-26`](../../../CHANGELOG.md) -- removed stale references to deleted governance/FAQ/releasing surfaces and corrected the render note now that the repo no longer carries the old local art bundle.
- [`README.md:95`](../../../README.md) and [`docs/market_surface.json:26`](../../market_surface.json) -- aligned the evaluator contact on `architects@zer0pa.ai`.
- [`docs/ARCHITECTURE.md:17,33-34`](../../ARCHITECTURE.md) and [`proofs/artifacts/2026-03-21_operator_status/README.md:22-26`](../../../proofs/artifacts/2026-03-21_operator_status/README.md) -- rerouted live doc interpretation away from missing proof-summary files and onto the current README plus supporting docs.
- [`proofs/artifacts/2026-03-22_docs_owner_pass/DOCS_FALSIFICATION_REPORT_2026-03-22.md:3-5`](../../../proofs/artifacts/2026-03-22_docs_owner_pass/DOCS_FALSIFICATION_REPORT_2026-03-22.md) -- marked the report as a dated historical audit so its old path references are not read as current-state routing.

## Clarity

- [`docs/LEGAL_BOUNDARIES.md:3`](../../LEGAL_BOUNDARIES.md) -- replaced private-stage / negative-readiness language with a direct statement of the live proof boundary.
- [`code/README.md:39`](../../../code/README.md) -- rewrote the package-alignment note so it states what the report proves instead of what it refuses to claim.

## Consistency

- [`README.md:91-93,197-198`](../../../README.md) and [`docs/market_surface.json:4,23`](../../market_surface.json) -- aligned release posture and portfolio positioning across the main product surface and the machine-readable market surface.
- [`docs/ARCHITECTURE.md:17,33-42`](../../ARCHITECTURE.md) -- aligned the architecture map with the README's open-release-gates posture instead of mixing readiness language with missing live-deployment summaries.

## Framing

- [`README.md:184,198`](../../../README.md) and [`docs/market_surface.json:23`](../../market_surface.json) -- removed IMC umbrella/platform framing and restated Geo as an independent product in the Zer0pa portfolio.

## Beta posture

- [`README.md:6,91,197`](../../../README.md), [`docs/LEGAL_BOUNDARIES.md:3`](../../LEGAL_BOUNDARIES.md), [`docs/market_surface.json:4`](../../market_surface.json), and [`proofs/artifacts/2026-03-22_docs_owner_pass/DOCS_FALSIFICATION_REPORT_2026-03-22.md:39`](../../../proofs/artifacts/2026-03-22_docs_owner_pass/DOCS_FALSIFICATION_REPORT_2026-03-22.md) -- converted remaining negative readiness language to the always-in-beta frame while leaving open release gates explicit.

## Primitive scope

- [`README.md:30`](../../../README.md) -- kept the Compass-8 claim lane-local and tied it to the live implementation in [`code/zpe_geo/codec.py:61-69`](../../../code/zpe_geo/codec.py) and [`code/zpe_geo/maneuver.py:17-36`](../../../code/zpe_geo/maneuver.py) instead of broadening it to a portfolio-wide narrative.

## Honest limits

- [`README.md:90-93`](../../../README.md) and [`CHANGELOG.md:28-31`](../../../CHANGELOG.md) -- preserved the blocked release-gate surface and did not soften the repo's explicit limits during the reorientation pass.
