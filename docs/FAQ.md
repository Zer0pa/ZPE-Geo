<p>
  <img src="../.github/assets/readme/zpe-masthead.gif" alt="ZPE Geo Masthead" width="100%">
</p>

# FAQ

For collaborators and auditors reading the Git-backed repo cold.

<p>
  <img src="../.github/assets/readme/section-bars/what-this-is.svg" alt="WHAT THIS IS" width="100%">
</p>

### What should I read first?

Start with [../proofs/FINAL_STATUS.md](../proofs/FINAL_STATUS.md), then [../PUBLIC_AUDIT_LIMITS.md](../PUBLIC_AUDIT_LIMITS.md), then [../AUDITOR_PLAYBOOK.md](../AUDITOR_PLAYBOOK.md). Those three files establish what is true now, what remains blocked, and how to inspect the repo honestly.

### What is ZPE Geo?

ZPE Geo is the deterministic geospatial trajectory workstream repo: package code, scripts, fixtures, proof surfaces, and documentation for AV-style XY trajectories, AIS-style WGS84 vessel trajectories, maneuver search, latency checks, and H3 roundtrip consistency.

### What is the strongest current statement this repo can make?

The repo can currently say that the March 21 copied-back operator pack still leaves `GEO-C001`, `GEO-C002`, and `GEO-C004` unresolved, so the repo is not release-ready. See [../proofs/FINAL_STATUS.md](../proofs/FINAL_STATUS.md).

### What counts as current truth versus historical truth?

Current truth is governed by [../proofs/FINAL_STATUS.md](../proofs/FINAL_STATUS.md), which interprets the copied-back March 21 operator pack under [../proofs/artifacts/2026-03-21_operator_status/](../proofs/artifacts/2026-03-21_operator_status/). Historical truth is the archived February 20 generated bundle under [../proofs/artifacts/2026-02-20_zpe_geo_wave1/](../proofs/artifacts/2026-02-20_zpe_geo_wave1/).

### Do the archived metrics still matter?

Yes. They remain historical evidence inside the repo. They do not, by themselves, authorize a current release statement. See [../proofs/CONSOLIDATED_PROOF_REPORT.md](../proofs/CONSOLIDATED_PROOF_REPORT.md).

### What exactly is the comparator claim?

The repo preserves a historical in-repo AIS baseline comparison in the archived bundle. That is not the same as claiming current parity closure or general superiority over outside systems. See [../proofs/CONSOLIDATED_PROOF_REPORT.md](../proofs/CONSOLIDATED_PROOF_REPORT.md).

### What stays outside the repo?

Secrets, raw `third_party/`, full external corpora, and uncopied outer-workspace orchestration material stay outside the repo unless explicitly copied back. See [LEGAL_BOUNDARIES.md](LEGAL_BOUNDARIES.md).

<p>
  <img src="../.github/assets/readme/section-bars/setup-and-verification.svg" alt="SETUP AND VERIFICATION" width="100%">
</p>

### How do I run the lowest-cost local verification path?

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -e "./code[dev,h3]"
python -m pytest code/tests -q
python - <<'PY'
from zpe_geo import H3Bridge
print(H3Bridge().backend)
PY
```

That verifies the repo-local package surface only.

### What does this not prove?

It does not prove blind-clone success, current full-corpus closure, or public-release readiness.

### Why do some files look contradictory?

Because the repo preserves historical generated artifacts rather than rewriting them. The current interpretation layer is [../proofs/FINAL_STATUS.md](../proofs/FINAL_STATUS.md); the detailed contradiction list is in [../proofs/CONSOLIDATED_PROOF_REPORT.md](../proofs/CONSOLIDATED_PROOF_REPORT.md).

### Where do bugs, proof disputes, and security issues go?

Use [SUPPORT.md](SUPPORT.md) for bug and proof-surface routing. Use [../SECURITY.md](../SECURITY.md) for vulnerabilities or secret exposure.
