<p>
  <img src=".github/assets/readme/zpe-masthead.gif" alt="ZPE Geo Masthead" width="100%">
</p>

# Contributing

This repo is a private staged workstream surface. Contributions must improve the repo without weakening the evidence boundary.

Read [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) and [LICENSE](LICENSE) before opening a change.

<p>
  <img src=".github/assets/readme/section-bars/before-you-start.svg" alt="BEFORE YOU START" width="100%">
</p>

## Scope Discipline

1. Touch repo-local material only: `code/`, `docs/`, `proofs/`, `.github/`, and root repo docs.
2. Do not reintroduce outer-shell material such as `.env`, `data/external_samples/`, raw `third_party/`, or ad hoc orchestration reports into git unless there is an explicit copy-back decision.
3. Do not proliferate new repos for the same workstream. This repo is the Git-backed authority surface.

<p>
  <img src=".github/assets/readme/section-bars/evidence-and-claims.svg" alt="EVIDENCE AND CLAIMS" width="100%">
</p>

## Evidence Discipline

1. Preserve archived generated proof artifacts even when they are inconvenient.
2. If a document cites a metric, verdict, or contradiction, route it to the canonical artifact instead of creating a second warehouse.
3. Do not rewrite accepted proofs to improve the story. Add clarifying docs, registries, or status notes around them instead.
4. Unresolved contradictions block merge. They are not copy problems.
5. Keep the repo URL, license summary, GIF asset paths, and front-door routing consistent with the current docs standard across root docs and `docs/`.

## Package And Proof Discipline

1. Keep `code/` installable and truthful to the repo-local package surface.
2. Keep `proofs/` readable and navigable for both current operator state and archived bundle state.
3. Reuse ZPE-IMC structure if helpful, but never import ZPE-IMC claims.

<p>
  <img src=".github/assets/readme/section-bars/install.svg" alt="INSTALL" width="100%">
</p>

## Before Opening A Change

Run the lowest-cost truthful check for the surface you touched.

Package and test surface:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -e "./code[dev,h3]"
python -m pytest code/tests -q
```

Docs surface:

- verify asset paths by document depth
- verify repo URL, contact, license, and authority references
- verify that current operator truth and historical bundle truth are not blurred
