# Auditor Playbook

This is the shortest honest audit path for the staged ZPE Geo repo.

It is not a substitute for Phase 5 blind-clone verification, and it does not convert mixed evidence into a pass.

## Shortest Audit Path

1. Read `README.md` for the staged repo contract and current phase boundary.
2. Read `proofs/FINAL_STATUS.md` for the current staged verdict and explicit deferrals.
3. Read `proofs/CONSOLIDATED_PROOF_REPORT.md` for the claim table, contradictions, and evidence anchors.
4. Inspect the core evidence files in `proofs/artifacts/2026-02-20_zpe_geo_wave1/`:
   - `claim_status_delta.md`
   - `quality_gate_scorecard.json`
   - `geo_av_benchmark.json`
   - `geo_ais_benchmark.json`
   - `geo_av_fidelity.json`
   - `geo_ais_fidelity.json`
   - `geo_maneuver_search_eval.json`
   - `geo_query_latency_benchmark.json`
   - `geo_stream_latency.json`
   - `geo_h3_roundtrip_results.json`
   - `residual_risk_register.md`
   - `max_gate_matrix.json`
   - `max_claim_resource_map.json`
   - `net_new_gap_closure_matrix.json`
5. Read `PUBLIC_AUDIT_LIMITS.md` before treating any archived bundle statement as a current public claim.

## Optional Low-Cost Local Check

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -e "./code[dev]"
python - <<'PY'
from zpe_geo import H3Bridge
print(H3Bridge().backend)
PY
```

This checks repo layout and package import only. Full rerun, blind clone, and performance augmentation are out of scope for the current phase.
