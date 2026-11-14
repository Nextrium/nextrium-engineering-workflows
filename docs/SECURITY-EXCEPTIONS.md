# Security Exceptions

All entries below are narrowly scoped and reviewable. An exception does not expire automatically: it remains valid only while its documented rationale and exact scope remain true. Review exceptions quarterly and whenever the affected fixture, scanner configuration, or ignore entry changes. Remove an exception as soon as its underlying condition no longer exists.

| ID | Finding | Scope | Rationale | Owner | Last reviewed | Review cadence | Status |
|---|---|---|---|---|---|---|---|
| SECEX-001 | Gitleaks `aws-access-token` | Two exact fingerprints in commit `416a68b1b4613acc6846a1778ba349df9179f674`, file `.github/workflows/security-baseline.yml`, lines 49 and 59 | Historical scanner-test fixtures used public dummy values. The fixture was subsequently changed to runtime construction so no token-like literal remains in the current file. The two historical fingerprints are ignored individually; no path-wide or rule-wide suppression is used. | Nextrium Engineering | 2026-11-14 | Quarterly | Active; retain while these exact historical findings remain harmless test data |

No live credential was identified by this exception. If this assessment changes, revoke/rotate the credential and investigate repository history immediately. The ignore entries are limited to the exact commit, file, rule, and line fingerprints above.

## Review enforcement

The scheduled exception-review workflow checks that each exception has a valid `Last reviewed` date no more than 120 days old. A stale review fails that scheduled check and requires maintainer attention; it does not renew, extend, or silently approve the exception. A maintainer must verify the rationale and scope, then update the review date. The check validates review freshness, not the truth of the underlying security assessment.
