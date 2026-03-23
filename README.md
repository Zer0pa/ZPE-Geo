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
<p align="center">
  <a href="code/README.md"><img src="https://img.shields.io/badge/quick%20verify-package%20surface-e5e7eb?labelColor=111111" alt="Quick verify: package surface"></a>
  <a href="proofs/FINAL_STATUS.md"><img src="https://img.shields.io/badge/proof%20anchors-final%20status%20%2B%20operator%20pack-e5e7eb?labelColor=111111" alt="Proof anchors: final status and operator pack"></a>
  <a href="docs/ARCHITECTURE.md"><img src="https://img.shields.io/badge/architecture-repo%20map-e5e7eb?labelColor=111111" alt="Architecture: repo map"></a>
  <a href="PUBLIC_AUDIT_LIMITS.md"><img src="https://img.shields.io/badge/public%20limits-explicit%20boundary-e5e7eb?labelColor=111111" alt="Public limits: explicit boundary"></a>
  <a href="docs/README.md"><img src="https://img.shields.io/badge/docs-routing%20index-e5e7eb?labelColor=111111" alt="Docs routing index"></a>
</p>
<table align="center" width="100%" cellpadding="0" cellspacing="0">
  <tr>
    <td width="25%"><a href="#quickstart-and-license"><img src=".github/assets/readme/nav/quickstart-and-license.svg" alt="Quickstart And License" width="100%"></a></td>
    <td width="25%"><a href="#what-this-is"><img src=".github/assets/readme/nav/what-this-is.svg" alt="What This Is" width="100%"></a></td>
    <td width="25%"><a href="#current-authority"><img src=".github/assets/readme/nav/current-authority.svg" alt="Current Authority" width="100%"></a></td>
    <td width="25%"><a href="#go-next"><img src=".github/assets/readme/nav/go-next.svg" alt="Go Next" width="100%"></a></td>
  </tr>
</table>

<a id="quickstart-and-license"></a>
<h2 align="center">Quickstart And License</h2>

### Quick Verify

The steps below verify the current repo-local package surface. They do not prove blind-clone closure, full-corpus closure, or release readiness.

```bash
git clone https://github.com/Zer0pa/ZPE-Geo.git zpe-geo
cd zpe-geo
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

After a successful repo-local verification you should have:

- an editable install of the inner `code/` package surface
- passing lightweight repo-local tests under `code/tests`
- an importable `zpe_geo` surface without relying on outer-workspace material

### License Boundary

- This repo uses the same SAL v6.0 license text as the current `ZPE-IMC` reference surface.
- SPDX tag: `LicenseRef-Zer0pa-SAL-6.0`.
- Commercial or hosted use above the SAL threshold requires contact at `architects@zer0pa.ai`.
- `LICENSE` is the legal source of truth. Repo docs summarize it; they do not override it.

<p align="center">
  <img src=".github/assets/readme/zpe-masthead-option-3.4.gif" alt="ZPE Geo Upper Insert" width="100%">
</p>

<a id="what-this-is"></a>
<h2 align="center">What This Is</h2>

ZPE Geo is the Git-backed workstream repo for deterministic geospatial trajectory compression, fidelity checks, maneuver search, and H3 roundtrip validation.

This repo is the live GitHub surface for the Geo workstream's package code, proof custody, and documentation. It is not a release-ready repo, and the repo-local install path is a sanity check rather than a release validation claim.

Quickest outsider orientation:

<table width="100%" border="1" bordercolor="#111111" cellpadding="16" cellspacing="0">
  <tr>
    <td width="25%" valign="top" align="center"><a href="proofs/FINAL_STATUS.md"><code>proofs/FINAL_STATUS.md</code></a></td>
    <td width="25%" valign="top" align="center"><a href="PUBLIC_AUDIT_LIMITS.md"><code>PUBLIC_AUDIT_LIMITS.md</code></a></td>
    <td width="25%" valign="top" align="center"><a href="AUDITOR_PLAYBOOK.md"><code>AUDITOR_PLAYBOOK.md</code></a></td>
    <td width="25%" valign="top" align="center"><a href="code/README.md"><code>code/README.md</code></a></td>
  </tr>
</table>

<p align="center">
  <img src=".github/assets/readme/zpe-masthead-option-3.5.gif" alt="ZPE Geo Lower Insert" width="100%">
</p>

<a id="current-authority"></a>
<h2 align="center">Current Authority</h2>

| Question | Current answer | Canonical source |
| --- | --- | --- |
| What is the governing current-status document? | [proofs/FINAL_STATUS.md](proofs/FINAL_STATUS.md) | [proofs/FINAL_STATUS.md](proofs/FINAL_STATUS.md) |
| What supports that current-status document? | The copied-back March 21 operator pack under [proofs/artifacts/2026-03-21_operator_status/](proofs/artifacts/2026-03-21_operator_status/) | [proofs/artifacts/2026-03-21_operator_status/README.md](proofs/artifacts/2026-03-21_operator_status/README.md) |
| What is the current blocker state? | The lane is still blocked on `GEO-C001`, `GEO-C002`, and `GEO-C004` | [proofs/FINAL_STATUS.md](proofs/FINAL_STATUS.md) |
| What is not being claimed? | No blind-clone closure, no full-corpus closure, no public release readiness, and no open-ended superiority claim | [PUBLIC_AUDIT_LIMITS.md](PUBLIC_AUDIT_LIMITS.md) |
| What is the correct acquisition surface for this workstream? | `https://github.com/Zer0pa/ZPE-Geo.git` | [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) |

<p align="center">
  <img src=".github/assets/readme/zpe-masthead-option-3-2.gif" alt="ZPE Geo Mid Masthead" width="100%">
</p>

<h2 align="center">Runtime Proof Surface</h2>

| Evidence family | What it answers | Route |
| --- | --- | --- |
| Repo-local package sanity check | Does the install-facing package still import and pass lightweight tests? | [code/README.md](code/README.md) |
| Governing current repo verdict | What is true now about release posture and blocking claims? | [proofs/FINAL_STATUS.md](proofs/FINAL_STATUS.md) |
| Current supporting evidence | Which copied-back operator artifacts support the current verdict? | [proofs/artifacts/2026-03-21_operator_status/README.md](proofs/artifacts/2026-03-21_operator_status/README.md) |
| Historical custody surface | What was proved earlier and why does it stay historical-only? | [proofs/CONSOLIDATED_PROOF_REPORT.md](proofs/CONSOLIDATED_PROOF_REPORT.md) |

## Historical Context Only

The archived bundle under [proofs/artifacts/2026-02-20_zpe_geo_wave1/](proofs/artifacts/2026-02-20_zpe_geo_wave1/) remains part of the repo because it contains real historical evidence:

- archived performance metrics across all eight promoted claims
- archived comparator notes, including an in-repo AIS baseline comparison
- preserved contradictions that explain why archived success does not equal current release authorization

Read those facts as historical-only context through [proofs/CONSOLIDATED_PROOF_REPORT.md](proofs/CONSOLIDATED_PROOF_REPORT.md), not as current release status.

<p align="center">
  <img src=".github/assets/readme/zpe-masthead-option-3-3.gif" alt="ZPE Geo Lower Masthead" width="100%">
</p>

<a id="go-next"></a>
<h2 align="center">Go Next</h2>

| Need | Route |
| --- | --- |
| Current verdict and release posture | [proofs/FINAL_STATUS.md](proofs/FINAL_STATUS.md) |
| Detailed current evidence and historical bundle interpretation | [proofs/CONSOLIDATED_PROOF_REPORT.md](proofs/CONSOLIDATED_PROOF_REPORT.md) |
| Audit path | [AUDITOR_PLAYBOOK.md](AUDITOR_PLAYBOOK.md) |
| Audit limits and exclusions | [PUBLIC_AUDIT_LIMITS.md](PUBLIC_AUDIT_LIMITS.md) |
| Architecture and evidence map | [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) |
| Docs ownership map | [docs/CANONICAL_DOC_REGISTRY.md](docs/CANONICAL_DOC_REGISTRY.md) |
| FAQ and support | [docs/FAQ.md](docs/FAQ.md), [docs/SUPPORT.md](docs/SUPPORT.md) |
| Community conduct | [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) |
| Install surface | [code/README.md](code/README.md) |

<h2 align="center">Contributing, Security, Support</h2>

| Need | Route |
| --- | --- |
| Contribution rules and docs hygiene | [CONTRIBUTING.md](CONTRIBUTING.md) |
| Community conduct and evidence norms | [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) |
| Vulnerability reporting and secret-exposure handling | [SECURITY.md](SECURITY.md) |
| Reader routing and response expectations | [docs/SUPPORT.md](docs/SUPPORT.md) |

<p align="center">
  <img src=".github/assets/readme/zpe-masthead-option-3.6.gif" alt="ZPE Geo Authority Insert" width="100%">
</p>
