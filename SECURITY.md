# Security

## Scope

This repo is private-first. Secret exposure is a staging blocker.

## Rules

- Do not commit `.env` files or credential material.
- Do not commit operator-only dataset exports unless their release status is explicit.
- Do not commit raw `third_party/` payloads without a deliberate dependency decision.
- Treat stale absolute-path references as integrity issues, not cosmetic issues.

## Reporting

If you discover a security issue, secret leak, or unsafe tracked file, report it privately before any visibility change or wider distribution.

Contact: `architects@zer0pa.ai`
