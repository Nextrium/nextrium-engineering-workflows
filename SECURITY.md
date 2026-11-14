# Security Policy

## Reporting

Do not disclose vulnerabilities in public issues. Report suspected vulnerabilities privately to the Nextrium maintainers through the repository's GitHub private vulnerability reporting feature where available.

## Workflow security requirements

- Third-party actions and reusable workflows must be pinned to verified full commit SHAs.
- Workflows must declare least-privilege permissions.
- Untrusted pull-request code must not receive secrets or write-capable tokens.
- Scanner versions must be explicit. Downloaded release binaries require verified checksums. Go-installed tools must use an explicit module version and retain Go's module checksum-database verification (GOSUMDB); do not disable checksum verification.
- Suppressions require a documented owner, reason, affected component, exact scope, and recorded human review. Exceptions do not automatically expire; review them at least quarterly and remove them when their rationale or scope no longer holds. Automated checks reject missing, malformed, future-dated, or more than 120-day-old review dates; this is a freshness check, not automatic renewal.
- Security gates must fail closed when a required scanner or audit cannot run.

## Scope

This policy covers this repository's reusable automation. It does not claim that consuming repositories are secure merely because they call these workflows.
