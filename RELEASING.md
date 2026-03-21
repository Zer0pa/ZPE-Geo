<p>
  <img src=".github/assets/readme/zpe-masthead.gif" alt="ZPE Geo Masthead" width="100%">
</p>

# Releasing

<p>
  <img src=".github/assets/readme/section-bars/release-notes.svg" alt="RELEASING" width="100%">
</p>

This document defines the release gate for the ZPE Geo workstream repo.

Canonical anchors:

- Repository: `https://github.com/Zer0pa/ZPE-Geo`
- Contact: `architects@zer0pa.ai`

Current release decision: `DO NOT RELEASE`

<p>
  <img src=".github/assets/readme/section-bars/verification.svg" alt="VERIFICATION" width="100%">
</p>

## Hard Release Gates

These are sovereign blockers. If either row fails, the repo is not releasable.

| Gate | Required state | Current state | Canonical evidence |
| --- | --- | --- | --- |
| Current operator gate closed | Pass | Fail | [proofs/FINAL_STATUS.md](proofs/FINAL_STATUS.md) |
| Blind-clone verification closed | Pass | Fail | [proofs/FINAL_STATUS.md](proofs/FINAL_STATUS.md), [PUBLIC_AUDIT_LIMITS.md](PUBLIC_AUDIT_LIMITS.md) |

## Supporting Readiness Checks

These matter, but they do not override a failed hard release gate.

| Check | Current state | Canonical evidence |
| --- | --- | --- |
| Git-backed repo carries copied-back current operator evidence | Pass | [proofs/artifacts/2026-03-21_operator_status/README.md](proofs/artifacts/2026-03-21_operator_status/README.md) |
| GitHub-safe docs render coherently | Pass | [README.md](README.md), [docs/README.md](docs/README.md), [docs/CANONICAL_DOC_REGISTRY.md](docs/CANONICAL_DOC_REGISTRY.md) |
| Repo-local package install and lightweight tests are truthful | Pass | [code/README.md](code/README.md), [proofs/artifacts/2026-03-21_docs_owner_pass/pytest_code_tests.log](proofs/artifacts/2026-03-21_docs_owner_pass/pytest_code_tests.log) |
| License, contact, repo URL, and authority references are coherent | Pass | `LICENSE`, [README.md](README.md), [CITATION.cff](CITATION.cff), [SECURITY.md](SECURITY.md) |

<p>
  <img src=".github/assets/readme/section-bars/scope.svg" alt="SCOPE" width="100%">
</p>

This release gate covers:

- the Git-backed repo and its docs
- the repo-local package surface under `code/`
- the copied-back March 21 operator status pack
- the archived historical proof bundle and its documented limits

This release gate does not treat outside-repo operator material as part of the release surface unless it has been copied back into the repo or explicitly declared out of scope.

<p>
  <img src=".github/assets/readme/section-bars/downstream-action-items.svg" alt="DOWNSTREAM ACTION ITEMS" width="100%">
</p>

## Release-Blocking Work Still Open

1. Close or formally narrow the current red claims with evidence. Here, “narrow” means reducing the claim surface in [proofs/FINAL_STATUS.md](proofs/FINAL_STATUS.md) and related authority docs rather than narrating a soft pass.
2. Complete blind-clone verification on the Git-backed repo surface.
3. Keep the repo-local docs and copied-back evidence in sync with the active lane.
