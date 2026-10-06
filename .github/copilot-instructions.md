# Copilot instructions for subnetcalc

## Project
Tiny Python 3.10+ CLI that calculates AWS subnets. Code lives in `src/subnetcalc/`, tests in `tests/`.
Only the standard library is used at runtime (`ipaddress`, `argparse`). Do not add runtime dependencies.

## Git flow
- `main` = released versions only (tagged `vX.Y.Z`). `develop` = integration branch.
- Feature branches: `feature/GH-<issue>-<short-desc>` from `develop`.
- Release branches: `release/X.Y.Z` from `develop`. Hotfix branches: `hotfix/X.Y.Z` from `main`.
- Never commit directly to `main` or `develop`.

## Commit messages
Conventional commits with the GitHub issue number:
`<type>(GH-<issue>): <short imperative message>`
Types: feat, fix, refactor, test, docs, ci, chore. Example: `fix(GH-3): subtract 5 reserved AWS IPs`.

## Code style
- Type hints everywhere, small pure functions, docstrings on public functions.
- Raise `ValueError` for bad user input; the CLI turns it into exit code 2.
- Every change needs a pytest test. Test names describe the scenario.
