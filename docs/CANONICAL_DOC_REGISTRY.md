<p>
  <img src="../.github/assets/readme/zpe-masthead.gif" alt="ZPE Geo Masthead" width="100%">
</p>

# Canonical Doc Registry

This file is the ownership map for the ZPE Geo documentation surface.

Rules:

- promote a fact once, then route back to it
- do not create second warehouses of metrics or readiness claims
- keep current operator truth and historical bundle truth explicitly separate

<p>
  <img src="../.github/assets/readme/section-bars/summary.svg" alt="SUMMARY" width="100%">
</p>

| Document | Owns | First route from |
| --- | --- | --- |
| [../README.md](../README.md) | front-door summary and first-hop routing | repo entry |
| [../RELEASING.md](../RELEASING.md) | release gate and exit criteria | README |
| [../GOVERNANCE.md](../GOVERNANCE.md) | evidence and status semantics | README, CONTRIBUTING |
| [../CONTRIBUTING.md](../CONTRIBUTING.md) | contribution discipline | README, SUPPORT |
| [../SECURITY.md](../SECURITY.md) | security reporting policy | README, SUPPORT |
| [FAQ.md](FAQ.md) | plain-language reader questions | README, SUPPORT |
| [SUPPORT.md](SUPPORT.md) | support routing | README |
| [ARCHITECTURE.md](ARCHITECTURE.md) | package/proof/operator map | README, docs/README |
| [LEGAL_BOUNDARIES.md](LEGAL_BOUNDARIES.md) | repo-local versus outside-repo limits | README, ARCHITECTURE |
| [../code/README.md](../code/README.md) | install-facing package truth | README, ARCHITECTURE |
| [../AUDITOR_PLAYBOOK.md](../AUDITOR_PLAYBOOK.md) | shortest honest audit path | README, docs/README |
| [../PUBLIC_AUDIT_LIMITS.md](../PUBLIC_AUDIT_LIMITS.md) | what the repo can and cannot establish | README, AUDITOR_PLAYBOOK |
| [../proofs/FINAL_STATUS.md](../proofs/FINAL_STATUS.md) | governing current verdict and release posture | README, RELEASING |
| [../proofs/CONSOLIDATED_PROOF_REPORT.md](../proofs/CONSOLIDATED_PROOF_REPORT.md) | detailed current evidence, archived metrics, contradictions, and residual risks | README, FINAL_STATUS |
| [../proofs/artifacts/2026-03-21_operator_status/README.md](../proofs/artifacts/2026-03-21_operator_status/README.md) | copied-back March 21 operator pack contents | FINAL_STATUS, proof report |

<p>
  <img src="../.github/assets/readme/section-bars/evidence-and-claims.svg" alt="EVIDENCE AND CLAIMS" width="100%">
</p>

## Authority Stack

1. [../proofs/FINAL_STATUS.md](../proofs/FINAL_STATUS.md) governs the current repo verdict.
2. [../proofs/artifacts/2026-03-21_operator_status/](../proofs/artifacts/2026-03-21_operator_status/) supplies the supporting March 21 operator evidence used by that verdict.
3. [../proofs/artifacts/2026-02-20_zpe_geo_wave1/](../proofs/artifacts/2026-02-20_zpe_geo_wave1/) is historical evidence only.
4. [../PUBLIC_AUDIT_LIMITS.md](../PUBLIC_AUDIT_LIMITS.md) defines what the repo still cannot claim.
