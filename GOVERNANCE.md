<p>
  <img src=".github/assets/readme/zpe-masthead.gif" alt="ZPE Geo Masthead" width="100%">
</p>

# Governance

<p>
  <img src=".github/assets/readme/section-bars/what-this-is.svg" alt="WHAT THIS IS" width="100%">
</p>

This document defines the evidence and status discipline for the ZPE Geo workstream repo.

Canonical anchors:

- Repository: `https://github.com/Zer0pa/ZPE-Geo`
- Contact: `architects@zer0pa.ai`
- Legal source of truth: `LICENSE`

<p>
  <img src=".github/assets/readme/section-bars/evidence-and-claims.svg" alt="EVIDENCE AND CLAIMS" width="100%">
</p>

Governance baseline:

- Artifacts outrank summary prose when they disagree about current state.
- Current operator state and archived historical bundle state must stay explicitly separated.
- Unsupported claims are removed, downgraded, or marked historical rather than narrated into readiness.
- This repo is the Git-backed authority surface for package docs and copied-back compact evidence; outside-repo operator state is not promoted until it is copied back or explicitly marked as out of scope.

| Evidence class | What it means here | Canonical home |
| --- | --- | --- |
| Current operator truth | The latest copied-back operator state that reflects the current lane outcome | `proofs/artifacts/2026-03-21_operator_status/` |
| Historical bundle truth | Archived generated evidence from the 2026-02-20 wave bundle | `proofs/artifacts/2026-02-20_zpe_geo_wave1/` |
| Repo package truth | What the repo-local package, scripts, fixtures, and tests currently expose | `code/README.md`, `docs/ARCHITECTURE.md` |
| Outside-repo/operator-only truth | Resources or execution state still outside this repo boundary | `docs/LEGAL_BOUNDARIES.md`, `PUBLIC_AUDIT_LIMITS.md` |

<p>
  <img src=".github/assets/readme/section-bars/summary.svg" alt="STATUS SEMANTICS" width="100%">
</p>

| Term | Meaning |
| --- | --- |
| Current operator state | The latest copied-back operator evidence for current lane status |
| Historical bundle result | Archived generated evidence preserved for custody and comparison |
| Outside-repo or operator-only | Real but intentionally excluded from this repo until copied back |
| Deferred | Known work intentionally left open and not promoted as closed |
| Not release-ready | Current state when release gates still fail or major proof gaps remain |

<p>
  <img src=".github/assets/readme/section-bars/compatibility-commitments.svg" alt="COMPATIBILITY COMMITMENTS" width="100%">
</p>

The repo commits to:

- one Git-backed workstream repo, not proliferated clones for the same authority surface
- explicit evidence routing rather than duplicated metric warehouses
- preserved archived contradictions rather than cleaned-up rewrite history
- consistent license, contact, and acquisition references across docs

<p>
  <img src=".github/assets/readme/section-bars/escalation-path.svg" alt="ESCALATION PATH" width="100%">
</p>

Escalate to `architects@zer0pa.ai` when:

- a release statement would exceed current evidence
- a contradiction exists between current operator state and archived bundle wording
- a legal or licensing interpretation is needed
- a proposal would introduce a new repo surface for the same workstream
