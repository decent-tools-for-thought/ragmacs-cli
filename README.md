# ragmacs-cli

`ragmacs-cli` is a command-line wrapper for the functions in `ragmacs.el`.
It executes the corresponding `ragmacs--gptel-*` functions through your
running Emacs server (`emacsclient`).

Currently the source path for ragmacs is hardcoded at `RAGMACS_PATH = "/opt/emacs/elpa/ragmacs/ragmacs.el"`.

## Setup

```bash
uv sync
uv run ragmacs-cli --help
```

## Examples

```bash
# manual and node traversal
uv run ragmacs-cli manual_names
uv run ragmacs-cli manual_list_nodes emacs
uv run ragmacs-cli manual_node_contents emacs Top

# symbol / feature introspection
uv run ragmacs-cli symbol_exists org-roam-node-find
uv run ragmacs-cli feature org-roam
uv run ragmacs-cli features
uv run ragmacs-cli load_paths

# source and docs
uv run ragmacs-cli function_source find-file
uv run ragmacs-cli variable_source org-roam-directory
uv run ragmacs-cli function_documentation find-file
uv run ragmacs-cli variable_documentation org-roam-directory
uv run ragmacs-cli variable_global_value org-roam-directory
uv run ragmacs-cli library_source org-roam

# completions
uv run ragmacs-cli function_completions "info-"
uv run ragmacs-cli command_completions "org-roam-"
uv run ragmacs-cli variable_completions "org-roam-"

# eval
uv run ragmacs-cli elisp_eval "(+ 1 2 3)"

# testing helpers
uv run ragmacs-cli coerce_nil
uv run ragmacs-cli simulate_error
uv run ragmacs-cli async_tool done
uv run ragmacs-cli all_arg_types \
  --object-json '{"foo":42}' \
  --string hello \
  --array-json '[1,2,3]' \
  --null \
  --true \
  --false \
  --enum bar
```

## Notes

- Requires a running Emacs server.
- Pass `--server-file` if you use a non-default server socket.
- For a no-install module invocation, use `python -m ragmacs_cli ...`.

## Releases

Tagging `v<version>` builds and verifies the packaged distributions, then publishes them:

- `ragmacs_cli-<version>.tar.gz`
- `ragmacs_cli-<version>-py3-none-any.whl`
- `SHA256SUMS`
