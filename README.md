# Nextrium Engineering Workflows

Reusable, security-conscious GitHub Actions workflows for Nextrium projects.

## Design principles

- Projects own their caller workflows, triggers, required checks, and repository protection settings.
- Shared workflows provide repeatable language, security, dependency, and release checks.
- Pin every reusable workflow reference to a full commit SHA in consuming repositories.
- Use least-privilege `GITHUB_TOKEN` permissions and do not pass secrets unless a workflow explicitly requires them.
- Treat pull-request code as untrusted. Never expose deployment credentials to untrusted pull requests.
- A passing workflow is evidence for the checks it actually runs, not a blanket production-security certification.

## Available workflows

| Workflow | Purpose | Status |
|---|---|---|
| `go-ci.yml` | Go formatting, tests, vet, and static analysis | Initial implementation |
| `python-ci.yml` | Python formatting, lint, tests, and type checks where configured | Initial implementation |
| `typescript-ci.yml` | TypeScript/JavaScript install, lint, type-check, and tests where configured | Initial implementation |
| `security-baseline.yml` | Git-history secret detection, GitHub Actions static analysis, optional Go vulnerability analysis | Initial implementation; validation pending |
| Dependency review | Planned; action pin and repository compatibility must be verified before implementation | Not implemented |

Workflows are reusable through `workflow_call`. See `docs/CONSUMER-GUIDE.md` for caller examples and rollout guidance. Security-gate scope and implementation status are tracked in `docs/SECURITY-BASELINE.md`.

## Security policy

- Do not integrate Aegis Scan or Aegis Review from this repository at this stage.
- Do not use floating action tags in shared workflows. Third-party actions must be pinned to verified full commit SHAs.
- Scanner/tool versions and checksums must be explicit and updated through reviewed changes.
- Findings must not be silently suppressed. Exceptions require an owner, rationale, scope, and expiry date.
- High/critical findings block the relevant gate unless a documented, time-bound exception is approved.

## Scope boundaries

This repository provides reusable automation. It does not configure branch protection, organization rulesets, repository secrets, environments, or deployment approvals. Those remain separate controls in each consuming repository or the Nextrium organization.

## Maturity

These workflows are an initial implementation. They must be exercised in a dedicated test repository and then in each consumer before being made required checks. Do not describe them as production-validated until successful runs and negative tests have been recorded.
