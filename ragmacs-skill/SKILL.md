---
name: ragmacs-cli
description: Use the ragmacs-cli command-line wrapper for ragmacs Emacs introspection functions. Trigger when the user wants to inspect Emacs state, symbols, features, libraries, manuals, Info nodes, function/variable docs or source, completions, or evaluate Elisp through a running Emacs server from the shell.
---

# ragmacs-cli

Use this skill when working from shell with the tool named:

- `ragmacs-cli`

## Execute

- Run commands directly.
- If Emacs server is non-default, pass `--server-file <path>`.
- Preserve output exactly unless user asks for reformatting.

## Core Commands

- Manual and Info traversal:
  - `ragmacs-cli manual_names`
  - `ragmacs-cli manual_list_nodes <manual>`
  - `ragmacs-cli manual_node_contents <manual> <node>`
  - `ragmacs-cli symbol_in_manual <symbol>`

- Symbol and runtime introspection:
  - `ragmacs-cli symbol_exists <symbol>`
  - `ragmacs-cli feature <feature>`
  - `ragmacs-cli features`
  - `ragmacs-cli load_paths`

- Source and documentation:
  - `ragmacs-cli library_source <library_name>`
  - `ragmacs-cli source <symbol> [--type defvar|defface]`
  - `ragmacs-cli function_source <symbol>`
  - `ragmacs-cli variable_source <symbol>`
  - `ragmacs-cli function_documentation <symbol>`
  - `ragmacs-cli variable_documentation <symbol>`
  - `ragmacs-cli variable_global_value <symbol>`

- Completions:
  - `ragmacs-cli function_completions <prefix>`
  - `ragmacs-cli command_completions <prefix>`
  - `ragmacs-cli variable_completions <prefix>`

- Evaluation:
  - `ragmacs-cli elisp_eval "<single sexp>"`

- Testing helpers (only if user asks):
  - `ragmacs-cli simulate_error`
  - `ragmacs-cli coerce_nil`
  - `ragmacs-cli async_tool <later_val>`
  - `ragmacs-cli all_arg_types --object-json '{"foo":42}' --string hi --array-json '[1,2]' --null --true --false --enum bar`

## Workflow

1. Start with cheap discovery commands (`symbol_exists`, `function_completions`, `manual_names`).
2. Resolve specific targets (`function_source`, `manual_node_contents`, `library_source`).
3. Only use `elisp_eval` when direct introspection commands are insufficient.
4. When investigating manuals, prefer `manual_list_nodes` before fetching full node contents.
5. If output is very large, stream or summarize with a note that full output is available.

## Failure Handling

- If command cannot connect to Emacs server, retry with `--server-file` when available.
- If a symbol/library/manual is missing, report the exact missing identifier and continue with alternatives.
- Do not mutate Emacs state unless user explicitly asks.
