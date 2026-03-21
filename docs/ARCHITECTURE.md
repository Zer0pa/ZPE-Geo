<p>
  <img src="../.github/assets/readme/zpe-masthead.gif" alt="ZPE Geo Masthead" width="100%">
</p>

# Architecture

<p>
  <img src="../.github/assets/readme/section-bars/what-this-is.svg" alt="WHAT THIS IS" width="100%">
</p>

This document is the canonical package, proof, and evidence-custody map for the ZPE Geo repo.

Canonical anchors:

- Repository: `https://github.com/Zer0pa/ZPE-Geo`
- Contact: `architects@zer0pa.ai`
- Install-facing package root: [../code/](../code/)
- Historical archived bundle: [../proofs/artifacts/2026-02-20_zpe_geo_wave1/](../proofs/artifacts/2026-02-20_zpe_geo_wave1/)
- Current copied-back operator status pack: [../proofs/artifacts/2026-03-21_operator_status/](../proofs/artifacts/2026-03-21_operator_status/)

<p>
  <img src="../.github/assets/readme/section-bars/repo-shape.svg" alt="REPO SHAPE" width="100%">
</p>

| Surface | What it owns | Canonical path |
| --- | --- | --- |
| Front door | Current repo summary and first-hop routing | [../README.md](../README.md) |
| Package surface | Install-facing Python package, scripts, fixtures, and lightweight tests | [../code/](../code/) |
| Current verdict surface | Governing current repo status and release posture | [../proofs/FINAL_STATUS.md](../proofs/FINAL_STATUS.md) |
| Current supporting evidence | Copied-back March 21 operator status pack | [../proofs/artifacts/2026-03-21_operator_status/](../proofs/artifacts/2026-03-21_operator_status/) |
| Historical evidence | Archived February 20 generated bundle | [../proofs/artifacts/2026-02-20_zpe_geo_wave1/](../proofs/artifacts/2026-02-20_zpe_geo_wave1/) |
| Outside-repo operator resources | Heavy data, secrets, and uncopied orchestration state | outside repo boundary |

| Repo path | Role |
| --- | --- |
| [../code/zpe_geo/](../code/zpe_geo/) | import-facing module surface |
| [../code/scripts/](../code/scripts/) | repo-local gate and validation helpers |
| [../code/tests/](../code/tests/) | lightweight repo-local tests |
| [../code/fixtures/](../code/fixtures/) | small deterministic fixtures |
| [../docs/](../docs/) and root docs | documentation and policy surface |
| [../proofs/](../proofs/) | verdicts, reports, runbooks, archived bundle, and copied-back operator pack |

<p>
  <img src="../.github/assets/readme/section-bars/verification.svg" alt="VERIFICATION" width="100%">
</p>

| Evidence family | Primary source | Canonical interpretation layer |
| --- | --- | --- |
| Current release posture and current blocking claims | [../proofs/artifacts/2026-03-21_operator_status/phase0311_runpod/](../proofs/artifacts/2026-03-21_operator_status/phase0311_runpod/) | [../proofs/FINAL_STATUS.md](../proofs/FINAL_STATUS.md) |
| Historical compression, fidelity, latency, search, and H3 facts | [../proofs/artifacts/2026-02-20_zpe_geo_wave1/](../proofs/artifacts/2026-02-20_zpe_geo_wave1/) | [../proofs/CONSOLIDATED_PROOF_REPORT.md](../proofs/CONSOLIDATED_PROOF_REPORT.md) |
| Package-alignment and install-surface truth | [../proofs/artifacts/2026-03-21_operator_status/release_alignment/TECHNICAL_ALIGNMENT_REPORT.md](../proofs/artifacts/2026-03-21_operator_status/release_alignment/TECHNICAL_ALIGNMENT_REPORT.md) | [../code/README.md](../code/README.md) |

<p>
  <img src="../.github/assets/readme/section-bars/out-of-scope.svg" alt="OUT OF SCOPE" width="100%">
</p>

| Item | Status | Why excluded from current authority |
| --- | --- | --- |
| Blind-clone verification | Open | Not yet present in repo evidence |
| Full-corpus closure for `GEO-C001`, `GEO-C002`, `GEO-C004` | Open | Current copied-back operator pack still shows red claims |
| Raw heavy corpora and raw `third_party/` | Outside repo | Kept outside the Git-backed repo unless deliberately copied back |
| Public release or live deployment claim | Blocked | Current release gate is not closed |
