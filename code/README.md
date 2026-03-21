<p>
  <img src="../.github/assets/readme/zpe-masthead.gif" alt="ZPE Geo Masthead" width="100%">
</p>

# zpe-geo

Install-facing package surface for the ZPE Geo workstream repo.

This package surface is intentionally smaller than the broader outer workspace. It exposes the repo-local package, fixtures, scripts, and tests that ship inside this Git-backed repo.

---

<p>
  <img src="../.github/assets/readme/section-bars/install.svg" alt="INSTALL" width="100%">
</p>

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -e "./code[dev,h3]"
```

Optional extras currently declared here:

- `dev`
- `h3`

The package does not ship the full external corpora or raw vendored payloads used by heavier outer-workspace runs.

---

<p>
  <img src="../.github/assets/readme/section-bars/verification.svg" alt="VERIFICATION" width="100%">
</p>

```bash
python -m pytest code/tests -q
python - <<'PY'
from zpe_geo import H3Bridge, ManeuverSearchIndex, decode_trajectory, encode_trajectory
print("backend:", H3Bridge().backend)
print("search class:", ManeuverSearchIndex.__name__)
PY
```

The current copied-back package-alignment evidence is in:

- `../proofs/artifacts/2026-03-21_operator_status/release_alignment/TECHNICAL_ALIGNMENT_REPORT.md`

That report is current package-alignment evidence. It is not a release-ready claim.

---

<p>
  <img src="../.github/assets/readme/section-bars/public-api-contract.svg" alt="PUBLIC API CONTRACT" width="100%">
</p>

The repo-local import surface currently exposes:

- `zpe_geo.encode_trajectory`
- `zpe_geo.decode_trajectory`
- `zpe_geo.H3Bridge`
- `zpe_geo.ManeuverSearchIndex`

The install-facing metadata is defined in `pyproject.toml` under this directory.

---

<p>
  <img src="../.github/assets/readme/section-bars/optional-dependency-groups.svg" alt="OPTIONAL DEPENDENCY GROUPS" width="100%">
</p>

| Extra | Why it exists |
| --- | --- |
| `dev` | pytest and local verification tooling |
| `h3` | H3 backend dependency for roundtrip checks |

Heavy corpus and parity stacks are not exposed as declared extras in this inner repo package surface.
