"""Canonical path helpers for the staged repo layout."""

from __future__ import annotations

import os
from pathlib import Path

ARTIFACT_BUNDLE_NAME = "2026-02-20_zpe_geo_wave1"


def _default_repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


REPO_ROOT = Path(os.environ.get("ZPE_GEO_REPO_ROOT", _default_repo_root())).resolve()
OUTER_WORKSPACE_ROOT = REPO_ROOT.parent
CODE_ROOT = REPO_ROOT / "code"
FIXTURES_ROOT = CODE_ROOT / "fixtures"
PROOFS_ROOT = REPO_ROOT / "proofs"
ARTIFACT_ROOT = PROOFS_ROOT / "artifacts" / ARTIFACT_BUNDLE_NAME
RUNBOOKS_ROOT = PROOFS_ROOT / "runbooks"

REPO_THIRD_PARTY_ROOT = REPO_ROOT / "third_party"
OUTER_THIRD_PARTY_ROOT = OUTER_WORKSPACE_ROOT / "third_party"
EXTERNAL_DATA_ROOT = OUTER_WORKSPACE_ROOT / "data"
EXTERNAL_SAMPLES_ROOT = EXTERNAL_DATA_ROOT / "external_samples"


def preferred_third_party_root() -> Path:
    for candidate in (REPO_THIRD_PARTY_ROOT, OUTER_THIRD_PARTY_ROOT):
        if candidate.exists():
            return candidate
    return REPO_THIRD_PARTY_ROOT
