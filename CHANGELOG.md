# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

-

## [0.4.0] - 2026-04-09

### Added

- Rich console output with grouped panels for scan results
- `scan` shows dirty/ahead/behind/clean status per repo
- `--no-color` flag to disable colors
- `--version` flag to print the current version
- Rich dependency

## [0.3.0] - 2026-04-05

### Added

- `scan` command to discover and list repositories
- PyYAML dependency for reading `reposweep.yml`

## [0.2.0] - 2026-04-04

### Added

- `init` writes a default `reposweep.yml` with `roots`, `ignore`, and `max_depth`

### Changed

- Project root detection starts from the current working directory

## [0.1.0] - 2026-04-04

### Added

- Command parsing system using argparse.
- Root discovery to run commands from subfolders

## [0.0.2] - 2026-04-04

### Added

- MIT Liscence

## [0.0.1] - 2026-04-03

### Added

- Documentation files (README, CHANGELOG, CONTRIBUTING)

[0.4.0]: https://gitlab.com/neo-bend-reality/reposweep/-/compare/v0.3.0...HEAD/
[0.3.0]: https://gitlab.com/neo-bend-reality/reposweep/-/compare/v0.2.0...v0.3.0
[0.2.0]: https://gitlab.com/neo-bend-reality/reposweep/-/compare/v0.1.0...v0.2.0
[0.1.0]: https://gitlab.com/neo-bend-reality/reposweep/-/compare/v0.0.2...v0.1.0
[0.0.2]: https://gitlab.com/neo-bend-reality/reposweep/-/compare/v0.0.1...v0.0.2
[0.0.1]: https://gitlab.com/neo-bend-reality/reposweep/-/commit/1a7f2bafe12aece7a7f528d21b4cf519fec6a410
