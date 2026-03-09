# Contributing

This repo is in private staging. Keep changes scoped to the staged repo boundary.

## Rules

1. Touch only repo-local material under `code/`, `docs/`, `proofs/`, and root repo docs.
2. Do not reintroduce outer-shell material such as `.env`, `data/external_samples/`, raw `third_party/`, or sector-orchestrator reports into git.
3. Do not rewrite archived generated proof files to make the story cleaner. Add clarifying docs around them instead.
4. Keep sector-specific claims sector-specific. Reuse IMC structure, not IMC content.
5. Treat unresolved contradictions as blockers, not as wording problems.

## Before Asking For Phase 5

- keep repo structure coherent
- keep the proof surface navigable
- keep operator-only dependencies outside the repo
- keep sanity checks lightweight unless Phase 5 has been explicitly authorized
