# Security Baseline: Required Scope and Status

This document is the implementation contract for the shared security gate. A control is not considered implemented merely because it appears in this plan.

## Blocking controls planned

| Control | Required behaviour | Current status |
|---|---|---|
| Secret detection | Scan tracked files and full Git history for high-confidence credentials; fail on confirmed secrets; support narrowly scoped, documented and periodically reviewed exceptions | Initial implementation: Gitleaks 8.30.1 scans full Git history; controlled positive detection, clean negative input and redaction assertions run in the workflow; full-history scan previously passed with two exact historical test-fixture fingerprints ignored under SECEX-001 |
| Dependency vulnerabilities | Evaluate direct and transitive dependencies; fail on critical/high runtime vulnerabilities; report moderate/low; exceptions must be documented, approved and periodically reviewed | npm and pip audit steps exist; govulncheck is available as an opt-in Go job; unified severity/exception policy not implemented |
| Dependency licence policy | Enforce approved licence policy against resolved dependency graph; unknown licences require review; no blanket allow-list | Not implemented |
| GitHub Actions security | Static analysis of workflow files; block dangerous token permissions, unsafe expression use, untrusted code execution and unsafe privileged triggers | Initial implementation: zizmor action v0.8.1; validation and policy tuning pending |
| Container security | Scan built images for OS and application vulnerabilities; block critical/high; generate machine-readable report | Not implemented; no container workflow yet |
| Infrastructure-as-code | Scan Terraform and supported IaC files when present; block high-confidence critical/high misconfigurations | Not implemented |
| SBOM | Generate SPDX or CycloneDX SBOM for release artifacts and retain as release evidence | Not implemented |
| Security regression tests | Include negative authentication, authorization, tenant-isolation, input-validation and secrets-handling tests in project-owned suites | Project-owned; no shared runner yet |
| Supply-chain integrity | Pin actions/workflows to full SHAs, review dependencies, generate provenance where supported, and retain release evidence | Partial: action pins and Dependabot configuration in this repository |

## Severity and exception policy

- Critical and high findings block merges/releases by default.
- Moderate findings are reported and triaged; projects may choose stricter blocking.
- Low findings are reported and tracked.
- An exception must include: finding/advisory identifier, affected package or file, business/technical rationale, compensating control where applicable, accountable owner, approval, exact scope, last human review date and review cadence.
- Exceptions do not automatically expire. They remain valid only while the documented rationale and exact scope remain true; review each active exception at least quarterly and whenever the affected condition changes.
- Automated freshness checks reject missing, malformed, future-dated or more than 120-day-old review dates. The central validator also checks that every non-comment Gitleaks ignore entry maps to an active ledger row. This is not an automatic renewal or proof that the underlying rationale remains true.
- Remove an exception when its justification or underlying condition no longer holds. Never automatically approve, renew or broaden an exception.
- Never suppress a scanner failure, timeout, missing report, or unavailable database as if the scan passed.

## Secret detection requirements

- Scan repository content and Git history. Pull-request coverage depends on the caller's PR trigger and the fetched history; this workflow does not claim a dedicated PR-diff-only scanner.
- Redact secret values in logs and artifacts.
- A confirmed credential must be revoked/rotated; deleting it from the current commit is insufficient.
- Allowlist entries must be exact, justified, owned, and periodically reviewed.
- Never print matched secret values in job output.

## Dependency and licence requirements

- Inspect direct and transitive dependencies, including lockfiles.
- Record package name, version, ecosystem, advisory, severity, and fix version when available.
- Follow the human dependency and licence review process in `docs/ENGINEERING-STANDARDS.md`; the presence of licence metadata or an SBOM is not licence approval.
- No blanket allow-list is implied. MIT, Apache-2.0, BSD-family and PostgreSQL-style licences are candidates for review, not automatic approvals.
- Unknown, custom, missing, source-available or conflicting licence expressions require human review before adoption.
- Review direct and transitive dependencies, exact versions, notices and obligations relevant to the product's distribution model.
- Do not infer that a package is safe or commercially usable from its repository's popularity.

## GitHub Actions requirements

- All third-party actions and reusable workflows must use verified full 40-character commit SHAs.
- Default workflow permissions to none; grant the minimum at job level.
- Never expose write tokens, secrets, or deployment credentials to untrusted pull-request code.
- Avoid `pull_request_target` for workflows that check out or execute pull-request content.
- Validate expressions used in shell commands; pass untrusted values through environment variables and quote them.
- Require review for changes to `.github/workflows/**` and shared workflow definitions.

## Rollout and validation

1. Complete the remaining reusable scanners with pinned tool versions and verified checksums/SHAs.
2. Implemented Gitleaks workflow checks: controlled positive detection, clean negative input and secret-redaction assertion. The Git-history scan also runs in the workflow.
3. Implemented exception-validator unit tests: current review, exactly 120-day boundary, stale review, future-dated review, malformed/missing review date, missing ledger rows, malformed column count, typoed/stray/indented rows, inactive exception, empty-ledger mode and ignore-entry reconciliation.
4. Not yet implemented as dedicated automated failure-injection tests: scanner binary unavailable, network outage, malformed Gitleaks report, and scanner timeout. A normal command failure is expected to fail the job, but that is not equivalent to tested failure injection.
5. Run in a non-production repository and verify expected pass/fail behaviour, then record exact run IDs and consumer SHA pins.
6. Configure repository rulesets separately after successful validation.

See `docs/SECURITY-EXCEPTIONS.md` for the exact, periodically reviewed Gitleaks test-fixture exception.

## Explicit exclusions

- Aegis Scan and Aegis Review are not integrated by this repository at this stage.
- No deployment workflow or production credentials are introduced here.
- No claim of production readiness or complete security coverage is made.
