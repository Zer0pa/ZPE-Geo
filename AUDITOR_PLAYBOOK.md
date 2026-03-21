<p>
  <img src=".github/assets/readme/zpe-masthead.gif" alt="ZPE Geo Masthead" width="100%">
</p>

# Auditor Playbook

This is the shortest honest audit path for the ZPE Geo workstream repo.

It is not a substitute for blind-clone verification, and it does not convert the archived bundle into a current-green release claim.

<p>
  <img src=".github/assets/readme/section-bars/what-this-is.svg" alt="WHAT THIS IS" width="100%">
</p>

## Shortest Honest Path

1. Read [README.md](README.md) for the repo boundary and first-hop routes.
2. Read [proofs/FINAL_STATUS.md](proofs/FINAL_STATUS.md) for the current verdict.
3. Read [proofs/CONSOLIDATED_PROOF_REPORT.md](proofs/CONSOLIDATED_PROOF_REPORT.md) for detailed current evidence, historical metrics, and contradictions.
4. Read the copied-back current operator pack:
   - [proofs/artifacts/2026-03-21_operator_status/README.md](proofs/artifacts/2026-03-21_operator_status/README.md)
   - [proofs/artifacts/2026-03-21_operator_status/phase0311_runpod/handoff_manifest.json](proofs/artifacts/2026-03-21_operator_status/phase0311_runpod/handoff_manifest.json)
   - [proofs/artifacts/2026-03-21_operator_status/phase0311_runpod/max_claim_resource_map.json](proofs/artifacts/2026-03-21_operator_status/phase0311_runpod/max_claim_resource_map.json)
5. Read the archived bundle only after that:
   - [proofs/artifacts/2026-02-20_zpe_geo_wave1/claim_status_delta.md](proofs/artifacts/2026-02-20_zpe_geo_wave1/claim_status_delta.md)
   - [proofs/artifacts/2026-02-20_zpe_geo_wave1/geo_av_benchmark.json](proofs/artifacts/2026-02-20_zpe_geo_wave1/geo_av_benchmark.json)
   - [proofs/artifacts/2026-02-20_zpe_geo_wave1/geo_ais_benchmark.json](proofs/artifacts/2026-02-20_zpe_geo_wave1/geo_ais_benchmark.json)
   - [proofs/artifacts/2026-02-20_zpe_geo_wave1/geo_av_fidelity.json](proofs/artifacts/2026-02-20_zpe_geo_wave1/geo_av_fidelity.json)
   - [proofs/artifacts/2026-02-20_zpe_geo_wave1/geo_ais_fidelity.json](proofs/artifacts/2026-02-20_zpe_geo_wave1/geo_ais_fidelity.json)
   - [proofs/artifacts/2026-02-20_zpe_geo_wave1/geo_query_latency_benchmark.json](proofs/artifacts/2026-02-20_zpe_geo_wave1/geo_query_latency_benchmark.json)
   - [proofs/artifacts/2026-02-20_zpe_geo_wave1/geo_stream_latency.json](proofs/artifacts/2026-02-20_zpe_geo_wave1/geo_stream_latency.json)
   - [proofs/artifacts/2026-02-20_zpe_geo_wave1/geo_h3_roundtrip_results.json](proofs/artifacts/2026-02-20_zpe_geo_wave1/geo_h3_roundtrip_results.json)
   - [proofs/artifacts/2026-02-20_zpe_geo_wave1/residual_risk_register.md](proofs/artifacts/2026-02-20_zpe_geo_wave1/residual_risk_register.md)
6. Read [PUBLIC_AUDIT_LIMITS.md](PUBLIC_AUDIT_LIMITS.md) before turning any archived metric into a current release statement.

<p>
  <img src=".github/assets/readme/section-bars/verification.svg" alt="VERIFICATION" width="100%">
</p>

## Optional Local Sanity Check

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

This verifies the repo-local package surface only. It does not prove full-corpus closure or blind-clone readiness.
