# ragmacs-cli

[![Release](https://img.shields.io/github/v/release/decent-tools-for-thought/ragmacs-cli?sort=semver)](https://github.com/decent-tools-for-thought/ragmacs-cli/releases)
![Python](https://img.shields.io/badge/python-3.11%2B-blue)
![License](https://img.shields.io/badge/license-0BSD-green)

Command-line wrapper around `ragmacs.el` functions exposed through a running Emacs server.

> [!IMPORTANT]
> This codebase is entirely AI-generated. It is useful to me, I hope it might be useful to others, and issues and contributions are welcome.

## Why This Exists

- Call `ragmacs.el` capabilities from scripts and agents.
- Reuse an existing Emacs session through `emacsclient`.
- Keep the command surface easy to inspect and automate.

## Install

```bash
python -m pip install .
ragmacs-cli --help
```

For local development:

```bash
uv sync
uv run ragmacs-cli --help
```

## Quick Start

```bash
uv run ragmacs-cli manual_names
uv run ragmacs-cli function_documentation find-file
uv run ragmacs-cli variable_source org-roam-directory
uv run ragmacs-cli elisp_eval "(+ 1 2 3)"
```

## Requirements

- A running Emacs server.
- `emacsclient` on `PATH`.
- `ragmacs.el` available at the configured source path.

Pass `--server-file` if you use a non-default server socket.

## Development

```bash
uv run pytest
uv run ruff check .
uv run mypy
```

## Credits

This client is built around `ragmacs.el` and the Emacs server model. Credit goes to the upstream ragmacs and Emacs projects for the editor-side functionality this wrapper exposes.
