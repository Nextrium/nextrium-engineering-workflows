# Consumer Guide

## Calling a reusable workflow

Create a project-owned workflow in the consuming repository. Replace `<FULL_SHA>` with the full 40-character commit SHA of a reviewed commit in this repository. Do not use `@main`, a branch, or a movable tag for production callers.

```yaml
name: Go CI
on:
  pull_request:
  push:
    branches: [main]
permissions: {}
jobs:
  go:
    uses: Nextrium/nextrium-engineering-workflows/.github/workflows/go-ci.yml@<FULL_SHA>
    with:
      go-version: "1.25"
      working-directory: "."
```

Use one caller per relevant language/security gate, or compose multiple reusable workflows in one project workflow. The consuming repository controls triggers and required-check names.

## Shared workflow update and pin management

1. Review the upstream change, including workflow permissions, third-party action SHAs, inputs, shell use, untrusted pull-request handling and changed checks.
2. Validate the new revision in a non-critical repository or test branch, including negative cases and failure behavior.
3. Update the consumer's reusable-workflow reference to the reviewed full 40-character commit SHA. Do not use a floating branch or tag.
4. Record the selected SHA in the caller workflow and retain the validation run/PR as review evidence.
5. Repeat the process for each consumer; do not assume updating this central repository updates existing consumers.

## Rollout sequence

1. Add callers to a non-critical test repository first.
2. Run pull-request and push scenarios; inspect logs and permissions.
3. Test negative cases: deliberately malformed formatting, failing tests, and a vulnerable dependency in a disposable branch.
4. Confirm expected failures and ensure no secrets are available to untrusted PR code.
5. Roll out to one production project at a time.
6. Only then configure the exact check names as required in repository rulesets/branch protection.

## Project ownership and inputs

- Keep project-specific build, integration, migration, and deployment requirements in the consuming repository.
- Set language versions explicitly in project configuration where possible.
- Python projects should configure Ruff, mypy (if used), pytest, and dependency metadata.
- Node projects must commit `package-lock.json` and define lint/typecheck/test scripts where applicable.
- Go projects must commit `go.mod` and `go.sum`.
- A skipped optional step is not evidence that the corresponding quality control exists.

## Security boundaries

- Shared workflows use minimal token permissions. Consumer workflows should also declare top-level `permissions: {}` and grant only job-level permissions required.
- Never pass deployment credentials to pull-request jobs.
- Do not use `pull_request_target` to check out and execute untrusted PR code.
- Pin reusable workflow calls to full commit SHAs and review upstream changes before updating pins.
- Configure branch protection/rulesets separately where the repository plan supports enforcement; reusable workflows do not enforce merges or protect branches.
- Where enforcement is unavailable, use pull requests, maintainer review and relevant CI evidence as interim controls. This is weaker than enforced protection and must not be represented as equivalent.
- Apply the company-wide dependency and licence review process in [ENGINEERING-STANDARDS.md](ENGINEERING-STANDARDS.md) before adding or materially changing dependencies.
- Do not add Aegis Scan/Review integration until separately approved.
