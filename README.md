# RepoSweep

A lightweight toolkit for keeping repositories clean and consistent. Status: pre-alpha.
Current version: 0.4.0.

## Table of Contents

- Install
- Usage
- Contributing
- License

## Install

Not packaged yet. Run from source once the CLI is added.

Dependencies:
- Python 3.11+
- PyYAML (see `requirements.txt`)
- Rich (see `requirements.txt`)

## Usage

RepoSweep is designed to run from any subfolder inside an initialized project. It finds the project root by walking upward from the current working directory until it sees `reposweep.yml`.

Behavior notes:
- `init` can run outside a RepoSweep project and writes a default `reposweep.yml`.
- `init` writes default `roots`, `ignore`, and `max_depth` settings.
- `scan` loads config from the project root.
- `scan` groups repos into panels: Dirty, Behind, Ahead, Clean.
- `scan` marks dirty repos and shows ahead/behind counts when available.
- `roots` is a list of starting folders for scans ("." means the project root).
- If `roots` is a string, it is treated as a single entry.
- `ignore` is name-based: any directory whose name matches an entry is skipped.
- Missing root paths are skipped with a warning.
- If no repos are found, `scan` prints a friendly message.
- `--no-color` disables colored output.
- `--version` prints the current version.
- Other commands error if `reposweep.yml` is not found.

## Contributing

See `CONTRIBUTING.md`.

## License

MIT License.
