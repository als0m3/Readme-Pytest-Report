# Readme Pytest Report

An experimental Docker-based GitHub Action that runs pytest and writes a Markdown results table into a repository README through the GitHub API.

## Status

This earlier prototype needs further work before use as a CI quality gate. Its parser expects a specific pytest text format, can fail on unsuccessful or empty test runs, and does not reliably propagate pytest's exit code. The generated “coverage” value is the percentage of passing tests, **not code coverage**.

## How it works

- Runs tests from `/github/workspace/tests/`.
- Reads the generated `test_result.txt`.
- Replaces content between two `[Pytest Table]: <>` markers in `README.md`.
- Commits the updated README to the configured branch.

`action.yml` defines four inputs: `username`, `token`, `repo`, and `branch`. The token needs write access to repository contents; store it in GitHub Actions secrets and never in source code. The action currently targets a repository owned by the authenticated user.

## Maintenance priorities

Replace text parsing with structured test results, propagate failing exit codes, remove application-specific test dependencies from the container, and test the action before enabling README writes. The historical captured test output has been removed from the repository's current tree.

See [SECURITY.md](SECURITY.md) for private vulnerability reports.
