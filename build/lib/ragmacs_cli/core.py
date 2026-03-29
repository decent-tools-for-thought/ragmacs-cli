#!/usr/bin/env python3
"""
Command-line wrapper for ragmacs Emacs functions.

This tool forwards subcommands to the running Emacs instance via emacsclient
and invokes the corresponding `ragmacs--gptel-*` function.
"""

from __future__ import annotations

import argparse
import base64
import subprocess
import sys
from collections.abc import Iterable
from dataclasses import dataclass

RAGMACS_PATH = "/opt/emacs/elpa/ragmacs/ragmacs.el"


@dataclass(frozen=True)
class EvalRequest:
    func: str
    arg_forms: list[str]


def lisp_string(value: str) -> str:
    return '"' + value.replace("\\", "\\\\").replace('"', '\\"') + '"'


def build_eval_expr(func: str, args: Iterable[str]) -> str:
    arg_list = " ".join(args)
    return f"""
(progn
  (or (require 'ragmacs nil t)
      (load {lisp_string(RAGMACS_PATH)} nil t)
      (error "Could not load ragmacs"))
  (let* ((res ({func} {arg_list}))
         (s (if (stringp res) res (prin1-to-string res))))
    (base64-encode-string (encode-coding-string s 'utf-8) t)))
""".strip()


def build_async_eval_expr(later_val: str) -> str:
    callback = "(lambda (val) (setq ragmacs-cli--async-res val))"
    return f"""
(progn
  (or (require 'ragmacs nil t)
      (load {lisp_string(RAGMACS_PATH)} nil t)
      (error "Could not load ragmacs"))
  (setq ragmacs-cli--async-res nil)
  (ragmacs--gptel-async-tool {callback} {lisp_string(later_val)})
  (let* ((res ragmacs-cli--async-res)
         (s (if (stringp res) res (prin1-to-string res))))
    (base64-encode-string (encode-coding-string s 'utf-8) t)))
""".strip()


def decode_emacsclient_output(output: str) -> str:
    normalized = output.strip()
    if normalized.startswith('"') and normalized.endswith('"'):
        normalized = normalized[1:-1]
        normalized = normalized.encode("utf-8").decode("unicode_escape")
    return base64.b64decode(normalized).decode("utf-8")


def run_emacs_eval(expr: str, server_file: str | None) -> str:
    cmd = ["emacsclient", "-e", expr]
    if server_file:
        cmd[1:1] = ["--server-file", server_file]
    proc = subprocess.run(cmd, capture_output=True, text=True)
    if proc.returncode != 0:
        sys.stderr.write(proc.stderr)
        raise SystemExit(proc.returncode)
    return decode_emacsclient_output(proc.stdout)


def json_to_lisp_form(json_text: str) -> str:
    return (
        f"(json-parse-string {lisp_string(json_text)} "
        ":object-type 'alist :array-type 'list "
        ":null-object nil :false-object :false)"
    )


def resolve_eval_request(args: argparse.Namespace) -> EvalRequest:
    if args.cmd == "all_arg_types":
        return EvalRequest(
            func="ragmacs--gptel-all-arg-types",
            arg_forms=[
                json_to_lisp_form(args.object_json),
                lisp_string(args.string),
                json_to_lisp_form(args.array_json),
                "nil" if args.null else '"not-null"',
                "t" if args.true_value else "nil",
                "t" if args.false_value else "nil",
                lisp_string(args.enum),
            ],
        )
    if args.cmd == "symbol_exists":
        return EvalRequest("ragmacs--gptel-symbolp", [lisp_string(args.symbol)])
    if args.cmd == "manual_names":
        return EvalRequest("ragmacs--gptel-manual-names", [])
    if args.cmd == "manual_list_nodes":
        return EvalRequest("ragmacs--gptel-manual-list-nodes", [lisp_string(args.manual)])
    if args.cmd == "manual_node_contents":
        return EvalRequest(
            "ragmacs--gptel-manual-node-contents",
            [lisp_string(args.manual), lisp_string(args.node)],
        )
    if args.cmd == "symbol_in_manual":
        return EvalRequest("ragmacs--gptel-symbol-in-manual", [lisp_string(args.symbol)])
    if args.cmd == "feature":
        return EvalRequest("ragmacs--gptel-featurep", [lisp_string(args.feature)])
    if args.cmd == "features":
        return EvalRequest("ragmacs--gptel-features", [])
    if args.cmd == "load_paths":
        return EvalRequest("ragmacs--gptel-load-paths", [])
    if args.cmd == "library_source":
        return EvalRequest("ragmacs--gptel-library-source", [lisp_string(args.library_name)])
    if args.cmd == "source":
        arg_forms = [lisp_string(args.symbol)]
        if args.type:
            arg_forms.append(f"'{args.type}")
        return EvalRequest("ragmacs--gptel-source", arg_forms)
    if args.cmd == "function_completions":
        return EvalRequest("ragmacs--gptel-function-completions", [lisp_string(args.prefix)])
    if args.cmd == "command_completions":
        return EvalRequest("ragmacs--gptel-command-completions", [lisp_string(args.prefix)])
    if args.cmd == "variable_completions":
        return EvalRequest("ragmacs--gptel-variable-completions", [lisp_string(args.prefix)])
    if args.cmd == "function_source":
        return EvalRequest("ragmacs--gptel-function-source", [lisp_string(args.symbol)])
    if args.cmd == "variable_source":
        return EvalRequest("ragmacs--gptel-variable-source", [lisp_string(args.symbol)])
    if args.cmd == "function_documentation":
        return EvalRequest("ragmacs--gptel-function-documentation", [lisp_string(args.symbol)])
    if args.cmd == "variable_documentation":
        return EvalRequest("ragmacs--gptel-variable-documentation", [lisp_string(args.symbol)])
    if args.cmd == "variable_global_value":
        return EvalRequest("ragmacs--gptel-variable-global-value", [lisp_string(args.symbol)])
    if args.cmd == "elisp_eval":
        return EvalRequest("ragmacs--gptel-eval", [lisp_string(args.expression)])
    if args.cmd == "simulate_error":
        return EvalRequest("ragmacs--gptel-simulate-error", [])
    if args.cmd == "coerce_nil":
        return EvalRequest("ragmacs--gptel-coerce-nil", [])
    raise SystemExit(f"Unknown command: {args.cmd}")


def parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="ragmacs",
        description="Invoke ragmacs Emacs functions from the command line.",
    )
    p.add_argument("--server-file", help="Path to Emacs server file (optional).")
    sub = p.add_subparsers(dest="cmd")

    sub.add_parser("manual_names")

    q = sub.add_parser("symbol_exists")
    q.add_argument("symbol")

    q = sub.add_parser("manual_list_nodes")
    q.add_argument("manual")

    q = sub.add_parser("manual_node_contents")
    q.add_argument("manual")
    q.add_argument("node")

    q = sub.add_parser("symbol_in_manual")
    q.add_argument("symbol")

    q = sub.add_parser("feature")
    q.add_argument("feature")

    sub.add_parser("features")
    sub.add_parser("load_paths")

    q = sub.add_parser("library_source")
    q.add_argument("library_name")

    q = sub.add_parser("source")
    q.add_argument("symbol")
    q.add_argument("--type", choices=["defvar", "defface"])

    q = sub.add_parser("function_completions")
    q.add_argument("prefix")

    q = sub.add_parser("command_completions")
    q.add_argument("prefix")

    q = sub.add_parser("variable_completions")
    q.add_argument("prefix")

    q = sub.add_parser("function_source")
    q.add_argument("symbol")

    q = sub.add_parser("variable_source")
    q.add_argument("symbol")

    q = sub.add_parser("function_documentation")
    q.add_argument("symbol")

    q = sub.add_parser("variable_documentation")
    q.add_argument("symbol")

    q = sub.add_parser("variable_global_value")
    q.add_argument("symbol")

    q = sub.add_parser("elisp_eval")
    q.add_argument("expression")

    sub.add_parser("simulate_error")
    sub.add_parser("coerce_nil")

    q = sub.add_parser("all_arg_types")
    q.add_argument("--object-json", required=True)
    q.add_argument("--string", required=True)
    q.add_argument("--array-json", required=True)
    q.add_argument("--null", action="store_true")
    q.add_argument("--true", dest="true_value", action="store_true")
    q.add_argument("--false", dest="false_value", action="store_true")
    q.add_argument("--enum", required=True)

    q = sub.add_parser("async_tool")
    q.add_argument("later_val")

    return p


def main(argv: list[str] | None = None) -> int:
    cli_parser = parser()
    args = cli_parser.parse_args(argv)
    if args.cmd is None:
        cli_parser.print_help()
        return 0

    if args.cmd == "async_tool":
        expr = build_async_eval_expr(args.later_val)
        print(run_emacs_eval(expr, args.server_file), end="")
        return 0

    request = resolve_eval_request(args)
    expr = build_eval_expr(request.func, request.arg_forms)
    print(run_emacs_eval(expr, args.server_file), end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
