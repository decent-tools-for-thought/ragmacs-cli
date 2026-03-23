<div align="center">

# ragmacs-cli

[![Release](https://img.shields.io/github/v/release/decent-tools-for-thought/ragmacs-cli?sort=semver&color=16a34a)](https://github.com/decent-tools-for-thought/ragmacs-cli/releases)
![Python](https://img.shields.io/badge/python-3.11%2B-15803d)
![License](https://img.shields.io/badge/license-0BSD-22c55e)

Command-line bridge for calling `ragmacs.el` functions through a running Emacs server from scripts and agents.

</div>

> [!IMPORTANT]
> This codebase is entirely AI-generated. It is useful to me, I hope it might be useful to others, and issues and contributions are welcome.

## Map
- [Install](#install)
- [Functionality](#functionality)
- [Requirements](#requirements)
- [Quick Start](#quick-start)
- [Development](#development)
- [Credits](#credits)

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

## Functionality

### Manuals And Symbol Discovery
- `ragmacs-cli manual_names`: list available manuals.
- `ragmacs-cli manual_list_nodes <manual>`: list nodes in one manual.
- `ragmacs-cli manual_node_contents <manual> <node>`: fetch the contents of one manual node.
- `ragmacs-cli symbol_in_manual <symbol>`: find manual references for a symbol.
- `ragmacs-cli symbol_exists <symbol>`: check whether a symbol exists.

### Feature And Load-Path Introspection
- `ragmacs-cli feature <feature>`: check whether an Emacs feature is loaded.
- `ragmacs-cli features`: list loaded features.
- `ragmacs-cli load_paths`: list active load paths.
- `ragmacs-cli library_source <library>`: show the source location for a library.
- `ragmacs-cli source <symbol>`: show source for a symbol, optionally constrained by `--type defvar|defface`.

### Completions And Documentation
- `ragmacs-cli function_completions <prefix>`: list matching function names.
- `ragmacs-cli command_completions <prefix>`: list matching command names.
- `ragmacs-cli variable_completions <prefix>`: list matching variable names.
- `ragmacs-cli function_source <symbol>`: show function source.
- `ragmacs-cli variable_source <symbol>`: show variable source.
- `ragmacs-cli function_documentation <symbol>`: show function docs.
- `ragmacs-cli variable_documentation <symbol>`: show variable docs.
- `ragmacs-cli variable_global_value <symbol>`: show the global value of a variable.

### Evaluation And Helper Endpoints
- `ragmacs-cli elisp_eval <expression>`: evaluate Emacs Lisp through the server.
- `ragmacs-cli async_tool <later-val>`: exercise the async ragmacs tool callback path.
- `ragmacs-cli all_arg_types ...`: send object, string, array, null, boolean, and enum-style argument combinations through the bridge.
- `ragmacs-cli simulate_error`: trigger the error-path helper.
- `ragmacs-cli coerce_nil`: exercise nil-coercion behavior.

### Connection Control
- `ragmacs-cli --server-file <path> ...`: target a non-default Emacs server socket for any command.

## Requirements

- A running Emacs server.
- `emacsclient` on `PATH`.
- `ragmacs.el` available at the configured source path.

## Quick Start

```bash
uv run ragmacs-cli manual_names
uv run ragmacs-cli function_documentation find-file
uv run ragmacs-cli variable_source org-roam-directory
uv run ragmacs-cli elisp_eval "(+ 1 2 3)"
```

## Development

```bash
uv run pytest
uv run ruff check .
uv run mypy
```

## Credits

This client is built for `ragmacs.el` and the Emacs server model and is not affiliated with the upstream ragmacs project.

Credit goes to the ragmacs and Emacs projects for the editor-side functionality this wrapper exposes.
