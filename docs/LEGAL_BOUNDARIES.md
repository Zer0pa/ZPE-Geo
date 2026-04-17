# Legal Boundaries

This repo is a live always-in-beta product surface with explicit proof boundaries. It is not a claim that blind-clone or full-corpus release gates are closed.

## Boundary Rules

- repo-local code, copied-back compact operator evidence, and archived proof material are inside this repo
- operator-only data, secrets, and uncopied runtime payloads stay outside the repo
- preserved proof artifacts outrank summary prose when they disagree
- unresolved contradictions remain explicit and documented

## Repo-Local Versus Outside-Repo Material

| Surface | Current location | Notes |
| --- | --- | --- |
| Package, scripts, tests, fixtures | inside repo | under `code/` |
| Current copied-back compact operator status | inside repo | under `../proofs/artifacts/2026-03-21_operator_status/` |
| Historical generated wave bundle | inside repo | under `../proofs/artifacts/2026-02-20_zpe_geo_wave1/` |
| Raw heavy corpora, secrets, raw vendored payloads | outside repo | intentionally excluded unless explicitly copied back |

## Current Integrity Limits

- historical bundle files still contain stale absolute-path references
- the archived bundle preserves contradictions instead of rewriting them
- the copied-back March 21 operator pack still shows unresolved red claims

Those are evidence facts, not copy problems.
