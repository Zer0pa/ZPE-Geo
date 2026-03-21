# ZPE Geo Technical Alignment Report

Date: 2026-03-21

## Classification

Standalone Python package candidate with a script-backed authority harness and optional heavy-data/parity extras. Not a live public artifact yet.

## Target Architecture

- Keep `zpe_geo/` as the install-facing package.
- Keep `scripts/` as the gate harness implementation surface.
- Expose the claimed CLI through `zpe_geo.cli`, not directly through repo-local script paths.
- Ship the deterministic gate fixtures inside the package so a built wheel does not depend on the historical inner snapshot.
- Keep heavy corpus/parity/runtime integrations optional through extras rather than implicit base dependencies.

## Technical Changes

- Added packaged fixture resolution in `zpe_geo/fixtures.py`.
- Added install-facing CLI in `zpe_geo/cli.py`.
- Packaged deterministic fixture JSON files under `zpe_geo/fixtures/`.
- Updated `scripts/common.py` to prefer the packaged fixture root instead of the historical inner snapshot path.
- Updated `pyproject.toml` to:
  - add truthful optional extras for `open-data` and `parity`,
  - add build tooling to `dev`,
  - move console entry points behind `zpe_geo.cli`,
  - package fixture data,
  - constrain pytest discovery to the live top-level `tests/` surface.
- Added `tests/conftest.py` and `tests/test_cli.py`.
- Added `.github/workflows/package-verify.yml`.
- Added `runbooks/RUNBOOK_ZPE_GEO_PACKAGE_VERIFICATION.md`.

## Verification

- Live top-level pytest surface: `37 passed`
  - `artifacts/2026-03-21_zpe_geo_release_alignment/pytest_live_surface.log`
- Editable-install pytest surface with declared extras: `37 passed`
  - `artifacts/2026-03-21_zpe_geo_release_alignment/pytest_editable_install.log`
- Wheel build succeeded
  - `artifacts/2026-03-21_zpe_geo_release_alignment/build_wheel.log`
- Built wheel contains packaged fixtures
  - `artifacts/2026-03-21_zpe_geo_release_alignment/wheel_contents_fixtures.txt`
- Clean wheel install resolves fixtures from `site-packages/zpe_geo/fixtures` and imports the gate runner
  - `artifacts/2026-03-21_zpe_geo_release_alignment/wheel_install_verify.json`
- CI workflow YAML parsed successfully with two jobs
  - `artifacts/2026-03-21_zpe_geo_release_alignment/workflow_static_check.txt`

## Remaining Real Blocker

- The live top-level package surface is still separate from the mapped inner Git repo path (`zpe-geo`). The technical package surface is aligned, but GitHub-hosted workflow execution will remain staged until the authoritative release surface is backed by the repo that will actually carry the workflow.
