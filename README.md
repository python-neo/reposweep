# RepoSweep

A lightweight toolkit for keeping repositories clean and consistent. Status: pre-alpha.
Current version: 0.2.0.

## Table of Contents

- Install
- Usage
- Contributing
- License

## Install

Not packaged yet. Run from source once the CLI is added.

## Usage

RepoSweep is designed to run from any subfolder inside an initialized project. It finds the project root by walking upward from the current working directory until it sees `reposweep.yml`.

Behavior notes:
- `init` is the only command that can run outside a RepoSweep project.
- `init` writes a default `reposweep.yml` with `roots`, `ignore`, and `max_depth`.
- `roots` is a list of starting folders for scans ("." means current folder).
- `ignore` is name-based: any directory whose name matches an entry is skipped.
- Other commands error if `reposweep.yml` is not found.
- Commands can require a subcommand and/or extra arguments; missing or extra args raise errors.

## Contributing

See `CONTRIBUTING.md`.

## License

MIT License.
