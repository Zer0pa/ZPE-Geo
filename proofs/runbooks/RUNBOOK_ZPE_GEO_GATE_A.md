# RUNBOOK_ZPE_GEO_GATE_A

## Objective
Runbook-first offload completion with dataset lock, schema inventory freeze, seed declaration, and fallback policy before coding.

## Inputs
- `STARTUP_PROMPT_ZPE_GEO_SECTOR_AGENT_2026-02-20.md`
- `PRD_ZPE_GEO_SECTOR_EXPANSION_WAVE1_2026-02-20.md`
- Concept anchor and rubric references listed in master runbook.

## Predeclared Commands
1. `python3 code/scripts/gate_a_lock.py`
2. `python3 code/scripts/validate_artifacts.py --gate A`

## Expected Outputs
- `proofs/artifacts/2026-02-20_zpe_geo_wave1/dataset_lock.json`
- `proofs/artifacts/2026-02-20_zpe_geo_wave1/schema_inventory.json`
- `proofs/artifacts/2026-02-20_zpe_geo_wave1/resource_failures.log`
- `proofs/artifacts/2026-02-20_zpe_geo_wave1/gate_snapshots/gate_A/`

## Falsification Intent
- Try to invalidate dataset provenance completeness by checking missing schema/version/hash fields.
- Try to invalidate source availability assumptions by probing source access and recording failures.

## Pass Criteria
- Dataset lock includes source reference, snapshot id, and deterministic fixture hash.
- Schema inventory covers AV, AIS, `.zpgeo`, search index, and integration contract schemas.
- Substitution log exists if any source access fails.

## Fail Signatures
- Missing or empty dataset lock entries.
- Non-deterministic fixture hash across rerun.
- Gate A outputs absent.

## Rollback
- Rebuild Gate A artifacts from source scripts and rerun validation.

## Fallback
- If live/public datasets are inaccessible, lock schema-faithful synthetic fixtures with explicit comparability notes.
