# Nextrium Company-Wide Engineering Standards

- **Status:** Approved company-wide operating standard
- **Owner:** Nextrium Engineering
- **Applies to:** Nextrium-owned repositories and products, unless a stricter product, customer, regulatory, or contractual requirement applies
- **Last updated:** 2026-11-14

This document defines the operating practices that accompany the reusable workflows in this repository. It is a policy and implementation guide; a documented control is not automatically implemented or enforced in every consuming repository.

## 1. Shared engineering workflows

### Source of truth

This repository is the canonical source for reusable Nextrium GitHub Actions workflows. Product repositories should consume shared workflows rather than independently copying and maintaining equivalent CI/security logic.

The shared workflows currently provide initial Go, Python, TypeScript and security-baseline checks. Their maturity and coverage are stated in the repository README and security baseline. A workflow must not be described as production-validated merely because it exists here.

### Consumption requirements

1. Keep caller workflows, triggers, project-specific build/test steps, deployment logic and repository protection settings in the product repository.
2. Call reusable workflows using a verified, reviewed, full 40-character commit SHA. Never use `@main`, a branch name or a movable tag for a production caller.
3. Use least-privilege workflow and job permissions. Default permissions to none where supported, then grant only what the job needs.
4. Do not pass deployment credentials or privileged secrets to untrusted pull-request code.
5. Review the shared-workflow change and its security implications before updating a consumer's pinned SHA.
6. Validate a new workflow or material version change in a non-critical/test repository, including expected failure cases, before wider rollout.
7. Roll out to consuming repositories deliberately and record the exact pinned SHA and validation evidence.
8. Keep project-specific integration, migration, tenant-isolation, security and load tests in the product repository. Shared CI does not replace them.

### Updating shared workflows

- Changes to reusable workflows require pull-request review and relevant CI evidence.
- Pin third-party actions and reusable dependencies to verified immutable commit SHAs.
- State the upstream action/tool version in comments or documentation where practical.
- Review permissions, input handling, untrusted-code boundaries and changed behavior when updating a pin.
- Do not make a consumer's checks required until the workflow has been validated in that repository and the exact check names are known.
- A successful run proves only the checks actually executed; it is not a general security certification.

### Repository governance fallback

Each repository should use pull requests and maintainer review. Reviewers must inspect the change and relevant CI results before merge.

Where enforced branch protection or rulesets are unavailable under the current repository plan, manual maintainer review plus CI evidence is the interim control. This fallback is weaker than enforced controls and must not be represented as equivalent. Do not require a paid subscription or public repository visibility solely to continue engineering work. Revisit the control when acceptable enforcement becomes available.

## 2. Dependency and licence review

### Required review before adoption

Every new direct dependency, material dependency replacement, and dependency with a material licence/version change must be reviewed before it is accepted into a product.

Review the resolved dependency graph, not only the top-level package declaration. The review should capture:

- Package name, ecosystem, exact version and source.
- Direct or transitive status and why it is needed.
- Declared SPDX licence expression, or the exact licence file and source when no valid SPDX expression is available.
- Relevant licence text, notices, attribution and redistribution obligations.
- Whether the licence imposes source-disclosure, network-use, patent, trademark, notice, or other obligations relevant to the product's distribution and business model.
- Known vulnerabilities, maintenance/abandonment signals and available upgrade path.
- Reviewer, decision, date and any conditions.

Lockfiles and generated dependency inventories/SBOMs should be retained where the project's build system supports them. An SBOM is an inventory aid, not proof of licence compliance or security.

### Licence decision rules

1. Do not assume that a popular, permissively described, or previously used package is approved.
2. MIT, Apache-2.0, BSD-family and PostgreSQL-style licences are candidates for review, not a blanket pre-approved allow-list. Check the exact package version and all transitive dependencies.
3. Unknown, missing, custom, source-available, conflicting or ambiguous licence information requires human review before adoption.
4. Copyleft and network-copyleft licences require explicit review of the actual use, distribution model, linking/integration method and corresponding obligations. Do not automatically approve or reject solely from the licence label.
5. Where obligations or compatibility are unclear, pause adoption and obtain an appropriate legal/business review. Engineering must not invent a legal interpretation.
6. Preserve required copyright, attribution, licence and NOTICE files in source distributions, binaries, containers and product notices as applicable.
7. Record the decision and rationale. Re-review when the dependency version, licence, usage, distribution model or product business model materially changes.

### Approval boundary

A scanner, package manager, SBOM generator or green CI run may identify licence metadata and known findings. None of these tools independently approves a dependency or establishes legal compliance. Until a machine-enforced licence policy is separately approved and implemented, licence approval remains a documented human review.

## 3. Security exceptions

- Exceptions must be narrow, identifiable, owned and supported by a written rationale and compensating controls where applicable.
- Exceptions do not have automatic expiry dates. They remain valid only while the documented rationale and exact scope remain true.
- A maintainer must review each active exception at least quarterly and whenever the affected fixture, scanner behavior/configuration, rule or ignore entry changes.
- Record the date of the latest human review, review cadence, owner, scope and status.
- Remove an exception immediately when its underlying condition no longer exists or its justification is no longer valid.
- Automated freshness checks must reject missing, malformed, future-dated or more than 120-day-old review dates. The 120-day boundary is a stale-record safeguard, not an extension of the quarterly review requirement.
- Automation must never approve, renew, broaden or silently extend an exception. A passing freshness check does not establish that the underlying rationale remains true.
- Never suppress scanner outages, timeouts, malformed reports or missing evidence as successful scans.

See [Security Exceptions](SECURITY-EXCEPTIONS.md) for the active exception ledger and review enforcement.

## 4. Implementation and enforcement status

The standards above define the expected company-wide practice. Each product repository remains responsible for adopting the relevant callers, pinning a reviewed SHA, adding product-specific tests and configuring repository controls where available.

The shared workflow repository must keep its README, consumer guide and security baseline accurate about what is implemented, validated, pending or not enforced. Do not claim company-wide enforcement until adoption has been verified in the relevant repositories.

## 5. Central repository protection status

The central workflow repository is public and can use GitHub's public-repository branch protection/ruleset capabilities. Its `main` branch should require pull requests, maintainer approval and the relevant successful status checks once the required check names are verified.

**Configuration status: pending repository-owner/admin action.** The repository's branch protection endpoint is not readable through the currently connected GitHub integration, and no ruleset is visible through the available read interface. This document does not claim that protection is enabled. Until an owner verifies and configures it in GitHub repository settings, use pull requests, maintainer review and CI evidence as the interim control. This is an administrative configuration gap, not a reason to purchase a plan or change repository visibility.

## 6. Review

Review this standard at least annually and whenever the company changes its distribution model, dependency policy, repository governance capabilities, security requirements or shared workflow architecture.
