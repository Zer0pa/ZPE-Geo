<p align="center">
  <img src=".github/assets/readme/zpe-masthead.gif" alt="ZPE Geo Masthead" width="100%">
</p>

<h1 align="center">ZPE Geo</h1>

<p align="center">
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-SAL%20v6.0-e5e7eb?labelColor=111111" alt="License: SAL v6.0"></a>
  <a href="code/README.md"><img src="https://img.shields.io/badge/python-3.11%2B-e5e7eb?labelColor=111111" alt="Python 3.11+"></a>
  <a href="proofs/FINAL_STATUS.md"><img src="https://img.shields.io/badge/release%20posture-not%20release--ready-e5e7eb?labelColor=111111" alt="Release posture: not release-ready"></a>
  <a href="proofs/artifacts/2026-03-21_operator_status/README.md"><img src="https://img.shields.io/badge/current%20operator%20state-red%20claims%20remain-e5e7eb?labelColor=111111" alt="Current operator state: red claims remain"></a>
  <a href="proofs/artifacts/2026-02-20_zpe_geo_wave1/claim_status_delta.md"><img src="https://img.shields.io/badge/historical%20bundle-archived%20only-e5e7eb?labelColor=111111" alt="Historical bundle: archived only"></a>
</p>

<p>
  <img src=".github/assets/readme/section-bars/what-this-is.svg" alt="WHAT THIS IS" width="100%">
</p>

ZPE Geo is the Git-backed private workstream repo for deterministic geospatial trajectory compression, fidelity checks, maneuver search, and H3 roundtrip validation.

For collaborators with repo access, this is the working GitHub surface for package code, proof custody, and documentation. It is not a release-ready repo, and the local install path here is a sanity check, not release validation.

## Start Here

1. Read [proofs/FINAL_STATUS.md](proofs/FINAL_STATUS.md). This is the governing current-status document for this repo.
2. Read [PUBLIC_AUDIT_LIMITS.md](PUBLIC_AUDIT_LIMITS.md). This defines what the repo can and cannot currently prove.
3. Read [AUDITOR_PLAYBOOK.md](AUDITOR_PLAYBOOK.md) if you want the shortest honest review path.
4. Read [code/README.md](code/README.md) for the install-facing package surface.

## Current Authority

| Question | Current answer | Canonical source |
| --- | --- | --- |
| What is the governing current-status document? | [proofs/FINAL_STATUS.md](proofs/FINAL_STATUS.md) | [proofs/FINAL_STATUS.md](proofs/FINAL_STATUS.md) |
| What supports that current-status document? | The copied-back March 21 operator pack under [proofs/artifacts/2026-03-21_operator_status/](proofs/artifacts/2026-03-21_operator_status/) | [proofs/artifacts/2026-03-21_operator_status/README.md](proofs/artifacts/2026-03-21_operator_status/README.md) |
| What is the current blocker state? | The lane is still blocked on `GEO-C001`, `GEO-C002`, and `GEO-C004` | [proofs/FINAL_STATUS.md](proofs/FINAL_STATUS.md) |
| What is not being claimed? | No blind-clone closure, no full-corpus closure, no public release readiness, and no open-ended superiority claim | [PUBLIC_AUDIT_LIMITS.md](PUBLIC_AUDIT_LIMITS.md) |

<p align="center">
  <img src=".github/assets/readme/zpe-masthead-option-3-2.gif" alt="ZPE Geo Masthead Detail" width="100%">
</p>

<p>
  <img src=".github/assets/readme/section-bars/quickstart-and-license.svg" alt="QUICKSTART AND LICENSE" width="100%">
</p>

Use the package surface from [code/README.md](code/README.md) if you want the lowest-cost repo-local sanity path:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -e "./code[dev,h3]"
python -m pytest code/tests -q
python - <<'PY'
from zpe_geo import H3Bridge, ManeuverSearchIndex, decode_trajectory, encode_trajectory
print("zpe-geo import OK")
print("h3 backend:", H3Bridge().backend)
print("search surface:", ManeuverSearchIndex.__name__)
PY
```

That verifies the repo-local package surface only.

## Historical Context Only

The archived bundle under [proofs/artifacts/2026-02-20_zpe_geo_wave1/](proofs/artifacts/2026-02-20_zpe_geo_wave1/) remains part of the repo because it contains real historical evidence:

- archived performance metrics across all eight promoted claims
- archived comparator notes, including an in-repo AIS baseline comparison
- preserved contradictions that explain why archived success does not equal current release authorization

Read those facts as historical-only context through [proofs/CONSOLIDATED_PROOF_REPORT.md](proofs/CONSOLIDATED_PROOF_REPORT.md), not as current release status.

<p align="center">
  <img src=".github/assets/readme/zpe-masthead-option-3-3.gif" alt="ZPE Geo Masthead Lower Detail" width="100%">
</p>

<p>
  <img src=".github/assets/readme/section-bars/where-to-go.svg" alt="WHERE TO GO" width="100%">
</p>

| Need | Route |
| --- | --- |
| Current verdict and release posture | [proofs/FINAL_STATUS.md](proofs/FINAL_STATUS.md) |
| Detailed current evidence and historical bundle interpretation | [proofs/CONSOLIDATED_PROOF_REPORT.md](proofs/CONSOLIDATED_PROOF_REPORT.md) |
| Audit path | [AUDITOR_PLAYBOOK.md](AUDITOR_PLAYBOOK.md) |
| Audit limits and exclusions | [PUBLIC_AUDIT_LIMITS.md](PUBLIC_AUDIT_LIMITS.md) |
| Architecture and evidence map | [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) |
| Docs ownership map | [docs/CANONICAL_DOC_REGISTRY.md](docs/CANONICAL_DOC_REGISTRY.md) |
| FAQ and support | [docs/FAQ.md](docs/FAQ.md), [docs/SUPPORT.md](docs/SUPPORT.md) |
| Install surface | [code/README.md](code/README.md) |
