# Changelog

All notable release-surface changes to the ZPE Geo workstream repo are documented here.

Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).
This changelog tracks the repo-facing package, proof, and documentation surface. It does not rewrite the archived generated proof bundle.

---

### Unreleased

Docs-owner, authority-surface, and portfolio-framing alignment pass.

### Added

- `docs/ARCHITECTURE.md` as the canonical package/proof/operator-boundary map
- `docs/LEGAL_BOUNDARIES.md` for the explicit evidence boundary and claim limits
- `code/README.md` for the install-facing package surface
- `proofs/artifacts/2026-03-21_operator_status/` as the copied-back compact current operator status pack

### Changed

- README now distinguishes current operator truth, historical archived-bundle truth, and outside-repo/operator-only material
- repo docs now route readers explicitly instead of relying on staging shorthand
- proof docs now treat the 2026-02-20 wave bundle as historical evidence and the 2026-03-21 operator pack as the current operator status surface
- repo docs now render without broken local art or dead proof-summary routes

### Not Changed

- the archived 2026-02-20 generated proof bundle remains preserved rather than rewritten
- release gates remain open and blind-clone closure is not claimed
