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
- [Configuration](#configuration)
- [Quick Start](#quick-start)
- [Credits](#credits)

## Install
$$\color{#15803D}Install \space \color{#22C55E}Tool$$

```bash
python -m pip install .    # install the package
ragmacs-cli --help         # inspect the command surface
```

## Functionality
$$\color{#15803D}Manual \space \color{#22C55E}Lookup$$
- `ragmacs-cli manual_names`: list available manuals.
- `ragmacs-cli manual_list_nodes <manual>`: list nodes in one manual.
- `ragmacs-cli manual_node_contents <manual> <node>`: fetch the contents of one manual node.
- `ragmacs-cli symbol_in_manual <symbol>`: find manual references for a symbol.
- `ragmacs-cli symbol_exists <symbol>`: check whether a symbol exists.

$$\color{#15803D}Feature \space \color{#22C55E}Lookup$$
- `ragmacs-cli feature <feature>`: check whether an Emacs feature is loaded.
- `ragmacs-cli features`: list loaded features.
- `ragmacs-cli load_paths`: list active load paths.
- `ragmacs-cli library_source <library>`: show the source location for a library.
- `ragmacs-cli source <symbol>`: show source for a symbol, optionally constrained by `--type defvar|defface`.

$$\color{#15803D}Symbol \space \color{#22C55E}Docs$$
- `ragmacs-cli function_completions <prefix>`: list matching function names.
- `ragmacs-cli command_completions <prefix>`: list matching command names.
- `ragmacs-cli variable_completions <prefix>`: list matching variable names.
- `ragmacs-cli function_source <symbol>`: show function source.
- `ragmacs-cli variable_source <symbol>`: show variable source.
- `ragmacs-cli function_documentation <symbol>`: show function docs.
- `ragmacs-cli variable_documentation <symbol>`: show variable docs.
- `ragmacs-cli variable_global_value <symbol>`: show the global value of a variable.

$$\color{#15803D}Eval \space \color{#22C55E}Helpers$$
- `ragmacs-cli elisp_eval <expression>`: evaluate Emacs Lisp through the server.
- `ragmacs-cli async_tool <later-val>`: exercise the async ragmacs tool callback path.
- `ragmacs-cli all_arg_types ...`: send object, string, array, null, boolean, and enum-style argument combinations through the bridge.
- `ragmacs-cli simulate_error`: trigger the error-path helper.
- `ragmacs-cli coerce_nil`: exercise nil-coercion behavior.

$$\color{#15803D}Server \space \color{#22C55E}Control$$
- `ragmacs-cli --server-file <path> ...`: target a non-default Emacs server socket for any command.

## Configuration
$$\color{#15803D}Server \space \color{#22C55E}Setup$$

- A running Emacs server.
- `emacsclient` on `PATH`.
- `ragmacs.el` available at the configured source path.

## Quick Start
$$\color{#15803D}Try \space \color{#22C55E}Lookup$$

```bash
uv run ragmacs-cli manual_names                         # list available manuals
uv run ragmacs-cli function_documentation find-file    # inspect a function docstring
uv run ragmacs-cli variable_source org-roam-directory  # locate a variable definition
uv run ragmacs-cli elisp_eval "(+ 1 2 3)"              # evaluate Elisp through emacsclient
```

## Credits

This client is built for `ragmacs.el` and the Emacs server model and is not affiliated with the upstream ragmacs project.

Credit goes to the ragmacs and Emacs projects for the editor-side functionality this wrapper exposes.
