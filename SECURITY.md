<p>
  <img src=".github/assets/readme/zpe-masthead.gif" alt="ZPE Geo Masthead" width="100%">
</p>

# Security

<p>
  <img src=".github/assets/readme/section-bars/scope.svg" alt="SCOPE" width="100%">
</p>

This repo is private-first. Secret exposure, unsafe tracked files, and accidental operator-only data disclosure are blocking issues.

<p>
  <img src=".github/assets/readme/section-bars/reporting-a-vulnerability.svg" alt="REPORTING A VULNERABILITY" width="100%">
</p>

## Private Reporting

Report vulnerabilities, secret leaks, or unsafe tracked files privately to `architects@zer0pa.ai`.

Do not open a broad-distribution issue for:

- credential exposure
- leaked `.env` material
- operator-only dataset exports
- unsafe absolute paths that disclose sensitive machine context

<p>
  <img src=".github/assets/readme/section-bars/secret-scan.svg" alt="SECRET SCAN" width="100%">
</p>

## What To Include

- affected file or component
- reproduction or proof-of-concept if applicable
- impact and suspected exposure scope
- any known affected paths or generated artifacts

## Repo-Specific Rules

- Do not commit `.env` files or credential material.
- Do not commit operator-only dataset exports unless their release status is explicit.
- Do not commit raw `third_party/` payloads without a deliberate dependency decision.
- Treat stale absolute-path references as integrity issues, not cosmetic issues.
- If a copied-back operator artifact could expose secrets, strip or exclude it before commit.
