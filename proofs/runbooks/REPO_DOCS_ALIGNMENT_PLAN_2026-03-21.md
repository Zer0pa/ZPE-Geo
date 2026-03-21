# ZPE Geo Docs Alignment Plan

Date: 2026-03-21
Repo: /Users/Zer0pa/ZPE/ZPE Geo/zpe-geo
Authority playbook: /Users/Zer0pa/ZPE/ZPE Geo/zpe-geo/proofs/runbooks/REPO_DOCS_PLAYBOOK_CANONICAL_2026-03-21.md

## Objective

Bring the Git-backed ZPE Geo repo to the ZPE-IMC documentation standard without borrowing ZPE-IMC claims. The pass must make the repo honest about:

- what this repo proves
- what is historical only
- what remains operator-only or owner-deferred
- where the authority artifacts live
- what still blocks public-ready release posture

## Truth Constraints

- The inner repo is the documentation authority surface.
- The archived bundle under `proofs/artifacts/2026-02-20_zpe_geo_wave1/` is historical generated evidence, not a blanket current-green signal.
- Public-facing docs must not hide the contradiction between archived core-wave PASS claims and unresolved max-wave/full-corpus limits.
- Missing evidence must be marked as missing, deferred, historical, or operator-only.

## Planned Work

1. Copy ZPE-IMC visual assets needed for GitHub-safe rendering into this repo.
2. Rewrite the front door and support docs around a single authority block and a public-vs-operator truth split.
3. Add the missing supporting docs needed for a coherent release surface:
   - `CHANGELOG.md`
   - `CITATION.cff`
   - `GOVERNANCE.md`
   - `RELEASING.md`
   - `docs/CANONICAL_DOC_REGISTRY.md`
   - `docs/ARCHITECTURE.md`
   - `docs/FAQ.md`
   - `code/README.md`
4. Update existing docs that currently overstate or underspecify the repo:
   - `README.md`
   - `CONTRIBUTING.md`
   - `SECURITY.md`
   - `AUDITOR_PLAYBOOK.md`
   - `PUBLIC_AUDIT_LIMITS.md`
   - `docs/README.md`
   - `docs/SUPPORT.md`
   - `docs/LEGAL_BOUNDARIES.md`
   - `proofs/README.md`
   - `proofs/FINAL_STATUS.md`
   - `proofs/CONSOLIDATED_PROOF_REPORT.md`
5. Run a falsification pass against claim wording, asset paths, and local-vs-live coherence.
6. Verify GitHub-safe relative paths, package/install guidance, and repo cleanliness before syncing remote.

## Subagent Sequence

1. Drafter: front-door and authority narrative set.
2. Layout: asset placement and path discipline.
3. Copy Augmentor: support, contributing, and FAQ surfaces.
4. Tables and Design: registry, architecture, and status tables.
5. Data Verification: evidence cross-check against proof artifacts.
6. Aesthetic Design: GitHub-safe visual consistency pass.
7. Falsification: unsupported-claim and drift pass.

## Acceptance Check

- Root README and supporting docs agree on repo URL, acquisition path, authority artifact, and current limits.
- No ZPE-IMC claims are imported into ZPE Geo docs.
- Historical bundle claims are explicitly separated from current operator/open limits.
- Asset paths render from root and `docs/`.
- A repo-local falsification report exists.
