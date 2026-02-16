# ragmacs-cli

`ragmacs-cli` is a command-line wrapper for the functions in `ragmacs.el`.
It executes the corresponding `ragmacs--gptel-*` functions through your
running Emacs server (`emacsclient`).

Currently the source path for ragmacs is hardcoded at `RAGMACS_PATH = "/opt/emacs/elpa/ragmacs/ragmacs.el"`.

## Examples

```bash
# manual and node traversal
ragmacs-cli manual_names
ragmacs-cli manual_list_nodes emacs
ragmacs-cli manual_node_contents emacs Top

# symbol / feature introspection
ragmacs-cli symbol_exists org-roam-node-find
ragmacs-cli feature org-roam
ragmacs-cli features
ragmacs-cli load_paths

# source and docs
ragmacs-cli function_source find-file
ragmacs-cli variable_source org-roam-directory
ragmacs-cli function_documentation find-file
ragmacs-cli variable_documentation org-roam-directory
ragmacs-cli variable_global_value org-roam-directory
ragmacs-cli library_source org-roam

# completions
ragmacs-cli function_completions "info-"
ragmacs-cli command_completions "org-roam-"
ragmacs-cli variable_completions "org-roam-"

# eval
ragmacs-cli elisp_eval "(+ 1 2 3)"

# testing helpers
ragmacs-cli coerce_nil
ragmacs-cli simulate_error
ragmacs-cli async_tool done
ragmacs-cli all_arg_types \
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
