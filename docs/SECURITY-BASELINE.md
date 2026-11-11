# Security Baseline: Required Scope and Status

This document is the implementation contract for the shared security gate. A control is not considered implemented merely because it appears in this plan.

## Blocking controls planned

| Control | Required behaviour | Current status |
|---|---|---|
| Secret detection | Scan tracked files and full PR diff for high-confidence credentials; fail on confirmed secrets; support narrowly scoped, expiring suppressions | Initial implementation: Gitleaks 8.30.1 scans full Git history; suppression workflow not implemented |
| Dependency vulnerabilities | Evaluate direct and transitive dependencies; fail on critical/high runtime vulnerabilities; report moderate/low; exceptions must be time-bound | npm and pip audit steps exist; govulncheck is available as an opt-in Go job; unified severity/exception policy not implemented |
| Dependency licence policy | Enforce approved licence policy against resolved dependency graph; unknown licences require review; no blanket allow-list | Not implemented |
| GitHub Actions security | Static analysis of workflow files; block dangerous token permissions, unsafe expression use, untrusted code execution and unsafe privileged triggers | Not implemented |
| Container security | Scan built images for OS and application vulnerabilities; block critical/high; generate machine-readable report | Not implemented; no container workflow yet |
| Infrastructure-as-code | Scan Terraform and supported IaC files when present; block high-confidence critical/high misconfigurations | Not implemented |
| SBOM | Generate SPDX or CycloneDX SBOM for release artifacts and retain as release evidence | Not implemented |
| Security regression tests | Include negative authentication, authorization, tenant-isolation, input-validation and secrets-handling tests in project-owned suites | Project-owned; no shared runner yet |
| Supply-chain integrity | Pin actions/workflows to full SHAs, review dependencies, generate provenance where supported, and retain release evidence | Partial: action pins and Dependabot configuration in this repository |

## Severity and exception policy

- Critical and high findings block merges/releases by default.
- Moderate findings are reported and triaged; projects may choose stricter blocking.
- Low findings are reported and tracked.
- An exception must include: finding/advisory identifier, affected package or file, business/technical rationale, compensating control, accountable owner, approval, and expiry date.
- Exceptions must be reviewed before expiry. Expired exceptions fail the gate.
- Never suppress a scanner failure, timeout, missing report, or unavailable database as if the scan passed.

## Secret detection requirements

- Scan both repository content and pull-request changes.
- Redact secret values in logs and artifacts.
- A confirmed credential must be revoked/rotated; deleting it from the current commit is insufficient.
- Allowlist entries must be exact, justified, owned, and periodically reviewed.
- Never print matched secret values in job output.

## Dependency and licence requirements

- Inspect direct and transitive dependencies, including lockfiles.
- Record package name, version, ecosystem, advisory, severity, and fix version when available.
- Enforce Nextrium's approved licence policy only after the organisation's licence allow/deny policy is formally agreed.
- Unknown, custom, or conflicting licence expressions require human review.
- Do not infer that a package is safe or commercially usable from its repository's popularity.

## GitHub Actions requirements

- All third-party actions and reusable workflows must use verified full 40-character commit SHAs.
- Default workflow permissions to none; grant the minimum at job level.
- Never expose write tokens, secrets, or deployment credentials to untrusted pull-request code.
- Avoid `pull_request_target` for workflows that check out or execute pull-request content.
- Validate expressions used in shell commands; pass untrusted values through environment variables and quote them.
- Require review for changes to `.github/workflows/**` and shared workflow definitions.

## Rollout and validation

1. Complete the missing reusable scanners with pinned tool versions and verified checksums/SHAs.
2. Validate scanner outputs against controlled positive and negative fixtures.
3. Run in a non-production repository and verify expected pass/fail behaviour.
4. Test failure modes: scanner unavailable, network failure, malformed report, expired exception, and secret redaction.
5. Publish exact required check names and pin the shared workflow commit in each consumer.
6. Configure repository rulesets separately after successful validation.

## Explicit exclusions

- Aegis Scan and Aegis Review are not integrated by this repository at this stage.
- No deployment workflow or production credentials are introduced here.
- No claim of production readiness or complete security coverage is made.
