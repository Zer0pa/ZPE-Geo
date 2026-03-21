# Root Layout Audit

Date: 2026-03-22
Repo: /Users/Zer0pa/ZPE/ZPE Geo/zpe-geo

## Goal

Keep the Git-backed repo root intentionally minimal and free of duplicate routing docs, using the public ZPE-IMC repo root as the cleanliness reference.

## Finding

The root surface was already mostly disciplined. The only clear duplicate at repo top level was `SUPPORT.md`, which duplicated `docs/SUPPORT.md` without owning distinct truth.

## Action Taken

- Removed `/Users/Zer0pa/ZPE/ZPE Geo/zpe-geo/SUPPORT.md`.
- Kept `docs/SUPPORT.md` as the single support-routing surface.
- Updated `/Users/Zer0pa/ZPE/ZPE Geo/zpe-geo/proofs/runbooks/REPO_DOCS_ALIGNMENT_PLAN_2026-03-21.md` so the plan no longer refers to the deleted duplicate.

## Result

The root surface now contains only the intended repo-level governance, release, audit, and front-door documents plus the main directories `.github/`, `code/`, `docs/`, and `proofs/`.

## Remaining Root Posture

- No untracked root clutter.
- No duplicate support-routing doc at repo top level.
- Root is cleaner than the current local ZPE-IMC clone and consistent with the public ZPE-IMC GitHub root pattern of keeping support routing under `docs/`.
