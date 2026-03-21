<p>
  <img src=".github/assets/readme/zpe-masthead.gif" alt="ZPE Geo Masthead" width="100%">
</p>

# Changelog

All notable release-surface changes to the ZPE Geo workstream repo are documented here.

Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).
This changelog tracks the repo-facing package, proof, and documentation surface. It does not rewrite the archived generated proof bundle.

---

<p>
  <img src=".github/assets/readme/section-bars/unreleased.svg" alt="UNRELEASED" width="100%">
</p>

### Unreleased

Docs-owner and authority-surface alignment pass.

### Added

- `docs/CANONICAL_DOC_REGISTRY.md` as the single ownership map for the repo documentation surface
- `docs/ARCHITECTURE.md` as the canonical package/proof/operator-boundary map
- `docs/FAQ.md` for reader-facing repo questions
- `GOVERNANCE.md` and `RELEASING.md` for evidence and release-boundary control
- `code/README.md` for the install-facing package surface
- `proofs/artifacts/2026-03-21_operator_status/` as the copied-back compact current operator status pack

### Changed

- README now distinguishes current operator truth, historical archived-bundle truth, and outside-repo/operator-only material
- support, security, and contribution docs now route readers explicitly instead of relying on staging shorthand
- proof docs now treat the 2026-02-20 wave bundle as historical evidence and the 2026-03-21 operator pack as the current operator status surface
- GitHub-safe visual assets from the ZPE-IMC documentation system are now carried locally inside this repo

### Not Changed

- the archived 2026-02-20 generated proof bundle remains preserved rather than rewritten
- the repo still is not release-ready and does not claim blind-clone closure
