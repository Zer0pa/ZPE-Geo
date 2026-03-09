# Concept Open Questions Resolution

| Question | Resolution Status | Evidence / Rationale |
|---|---|---|
| Does Argoverse 2 Apache 2.0 allow commercial benchmark citation? | INCONCLUSIVE | Runtime lane did not fetch/legal-verify terms; tracked in risk register. Evidence: `dataset_lock.json`. |
| Is COG always present in AIS or must infer from delta? | RESOLVED | Fixture and falsification include invalid COG sentinel 511 handling with inference fallback. Evidence: `data/fixtures/ais_noaa_fixture_v1.json`, `falsification_results.md`. |
| Precision loss at H3 res 9 vs 11? | RESOLVED | Multi-resolution roundtrip and drift checks executed at 9/10/11. Evidence: `geo_h3_roundtrip_results.json`. |
| Does ACM 2025 release comparison datasets? | INCONCLUSIVE | Reference is included for framing; supplementary dataset availability not validated in lane runtime. Evidence: `dataset_lock.json`, `innovation_delta_report.md`. |
| Is Autoware plugin API stable for production? | INCONCLUSIVE | Integration contract includes API stability pending upstream roadmap confirmation. Evidence: `integration_readiness_contract.json`. |
| Can UTM-like coordinates be encoded without re-projection? | RESOLVED | AV local XY coordinate path encoded directly in codec. Evidence: `geo_av_fidelity.json`. |
