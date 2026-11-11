# Security Policy

## Reporting

Do not disclose vulnerabilities in public issues. Report suspected vulnerabilities privately to the Nextrium maintainers through the repository's GitHub private vulnerability reporting feature where available.

## Workflow security requirements

- Third-party actions and reusable workflows must be pinned to verified full commit SHAs.
- Workflows must declare least-privilege permissions.
- Untrusted pull-request code must not receive secrets or write-capable tokens.
- Scanner versions must be explicit; downloaded binaries require verified checksums.
- Suppressions require a documented owner, reason, affected component, and expiry.
- Security gates must fail closed when a required scanner or audit cannot run.

## Scope

This policy covers this repository's reusable automation. It does not claim that consuming repositories are secure merely because they call these workflows.
