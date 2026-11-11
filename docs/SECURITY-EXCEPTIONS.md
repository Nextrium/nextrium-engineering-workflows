# Security Exceptions

All entries below are narrow, reviewable exceptions. Remove each exception when its underlying condition is no longer present. Expired exceptions must fail the security gate.

| ID | Finding | Scope | Rationale | Owner | Expiry | Status |
|---|---|---|---|---|---|---|
| SECEX-001 | Gitleaks `aws-access-token` | Two exact fingerprints in commit `416a68b1b4613acc6846a1778ba349df9179f674`, file `.github/workflows/security-baseline.yml`, lines 49 and 59 | A temporary scanner-test fixture used a public dummy value. The fixture was subsequently changed to runtime construction so no token-like literal remains in the current file. The two historical fingerprints are ignored individually; no path-wide or rule-wide suppression is used. | Nextrium Engineering | 2026-12-11 | Temporary; review required |

No live credential was identified by this exception. If this assessment changes, revoke/rotate the credential and investigate repository history immediately. The ignore entries are limited to the exact commit, file, rule, and line fingerprints above.
