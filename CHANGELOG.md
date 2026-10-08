# Changelog

## Unreleased

### Features

- **GH-3:** Add the `overlaps` CLI command for checking multiple CIDR blocks.

## 0.2.1

### Other

- Update CI branch triggers to use `master`.
- Ignore Python caches, virtual environments, and build artifacts.

## 0.2.0

### Features

- **GH-2:** Detect overlapping CIDR blocks and report the overlapping pairs.

### Fixes

- **GH-1:** Correct the AWS usable IP count by accounting for AWS-reserved addresses.

### Other

- **GH-5:** Remove the tracked `.DS_Store` file and ignore it going forward.
