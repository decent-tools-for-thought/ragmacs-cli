---
name: ragmacs-cli
description: Use the ragmacs command-line wrapper for ragmacs Emacs introspection functions. Trigger when the user wants to inspect Emacs state, symbols, features, libraries, manuals, Info nodes, function/variable docs or source, completions, or evaluate Elisp through a running Emacs server from the shell.
---

# ragmacs-cli

Use this skill when working from shell with the tool named:

- `ragmacs`

## Execute

- Run commands directly.
- If Emacs server is non-default, pass `--server-file <path>`.
- Preserve output exactly unless user asks for reformatting.

## Core Commands

- Manual and Info traversal:
  - `ragmacs manual_names`
  - `ragmacs manual_list_nodes <manual>`
  - `ragmacs manual_node_contents <manual> <node>`
  - `ragmacs symbol_in_manual <symbol>`

- Symbol and runtime introspection:
  - `ragmacs symbol_exists <symbol>`
  - `ragmacs feature <feature>`
  - `ragmacs features`
  - `ragmacs load_paths`

- Source and documentation:
  - `ragmacs library_source <library_name>`
  - `ragmacs source <symbol> [--type defvar|defface]`
  - `ragmacs function_source <symbol>`
  - `ragmacs variable_source <symbol>`
  - `ragmacs function_documentation <symbol>`
  - `ragmacs variable_documentation <symbol>`
  - `ragmacs variable_global_value <symbol>`

- Completions:
  - `ragmacs function_completions <prefix>`
  - `ragmacs command_completions <prefix>`
  - `ragmacs variable_completions <prefix>`

- Evaluation:
  - `ragmacs elisp_eval "<single sexp>"`

- Testing helpers (only if user asks):
  - `ragmacs simulate_error`
  - `ragmacs coerce_nil`
  - `ragmacs async_tool <later_val>`
  - `ragmacs all_arg_types --object-json '{"foo":42}' --string hi --array-json '[1,2]' --null --true --false --enum bar`

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
