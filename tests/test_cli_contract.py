from __future__ import annotations

import argparse

from ragmacs_cli import core


def test_bare_invocation_exits_zero_and_prints_help(capsys: object) -> None:
    assert core.main([]) == 0
    assert "usage: ragmacs-cli" in capsys.readouterr().out


def test_subtree_help_exits_zero(capsys: object) -> None:
    try:
        core.main(["symbol_exists", "--help"])
    except SystemExit as exc:
        assert exc.code == 0
    else:
        raise AssertionError("argparse help should exit")

    assert "usage: ragmacs-cli symbol_exists" in capsys.readouterr().out


def test_cli_wires_representative_arguments(monkeypatch: object, capsys: object) -> None:
    seen: dict[str, object] = {}

    def fake_run_emacs_eval(expr: str, server_file: str | None) -> str:
        seen["expr"] = expr
        seen["server_file"] = server_file
        return "RESULT"

    monkeypatch.setattr(core, "run_emacs_eval", fake_run_emacs_eval)

    exit_code = core.main(
        [
            "--server-file",
            "/tmp/emacs.sock",
            "all_arg_types",
            "--object-json",
            '{"foo":42}',
            "--string",
            "hello",
            "--array-json",
            "[1,2,3]",
            "--null",
            "--true",
            "--false",
            "--enum",
            "bar",
        ]
    )

    assert exit_code == 0
    assert capsys.readouterr().out == "RESULT"
    assert seen["server_file"] == "/tmp/emacs.sock"

    expected_request = core.resolve_eval_request(
        argparse.Namespace(
            cmd="all_arg_types",
            object_json='{"foo":42}',
            string="hello",
            array_json="[1,2,3]",
            null=True,
            true_value=True,
            false_value=True,
            enum="bar",
            server_file="/tmp/emacs.sock",
        )
    )
    assert seen["expr"] == core.build_eval_expr(expected_request.func, expected_request.arg_forms)
