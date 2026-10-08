# Changelog

## 0.2.0

### Features

- **GH-2:** Detect overlapping CIDR blocks and report the overlapping pairs.
- **GH-3:** Add the `overlaps` CLI command for checking multiple CIDR blocks.

### Fixes

- **GH-1:** Correct the AWS usable IP count by accounting for AWS-reserved addresses.

### Other

- **GH-5:** Remove the tracked `.DS_Store` file and ignore it going forward.
