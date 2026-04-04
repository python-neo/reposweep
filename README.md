# RepoSweep

A lightweight toolkit for keeping repositories clean and consistent. Status: pre-alpha.

## Table of Contents

- Install
- Usage
- Contributing
- License

## Install

Not packaged yet. Run from source once the CLI is added.

## Usage

RepoSweep is designed to run from any subfolder inside an initialized project. It finds the project root by walking upward until it sees `reposweep.yml`.

Behavior notes:
- `init` is the only command that can run outside a RepoSweep project.
- Other commands error if `reposweep.yml` is not found.
- Commands can require a subcommand and/or extra arguments; missing or extra args raise errors.

## Contributing

See `CONTRIBUTING.md`.

## License

MIT License.
