from __future__ import annotations

import argparse
import base64
import subprocess

import pytest

from ragmacs_cli import core


def parse_args(argv: list[str]) -> argparse.Namespace:
    return core.parser().parse_args(argv)


def test_lisp_string_escapes_quotes_and_backslashes() -> None:
    assert core.lisp_string('say "hi" \\ now') == '"say \\"hi\\" \\\\ now"'


def test_build_eval_expr_embeds_function_and_args() -> None:
    expr = core.build_eval_expr("ragmacs--gptel-featurep", ['"org-roam"'])

    assert '(ragmacs--gptel-featurep "org-roam")' in expr
    assert f"(load {core.lisp_string(core.RAGMACS_PATH)} nil t)" in expr
    assert "base64-encode-string" in expr


def test_build_async_eval_expr_uses_callback() -> None:
    expr = core.build_async_eval_expr("done")

    assert "ragmacs-cli--async-res" in expr
    assert "ragmacs--gptel-async-tool" in expr
    assert '"done"' in expr


def test_json_to_lisp_form_preserves_parser_flags() -> None:
    form = core.json_to_lisp_form('{"foo":[false,null]}')

    assert form == (
        '(json-parse-string "{\\"foo\\":[false,null]}" :object-type \'alist '
        ":array-type 'list :null-object nil :false-object :false)"
    )


@pytest.mark.parametrize(
    ("argv", "expected_func", "expected_args"),
    [
        (["manual_names"], "ragmacs--gptel-manual-names", []),
        (
            ["source", "find-file", "--type", "defvar"],
            "ragmacs--gptel-source",
            ['"find-file"', "'defvar"],
        ),
        (
            [
                "all_arg_types",
                "--object-json",
                '{"foo":42}',
                "--string",
                "hello",
                "--array-json",
                "[1,2,3]",
                "--null",
                "--true",
                "--enum",
                "bar",
            ],
            "ragmacs--gptel-all-arg-types",
            [
                (
                    '(json-parse-string "{\\"foo\\":42}" '
                    ":object-type 'alist :array-type 'list "
                    ":null-object nil :false-object :false)"
                ),
                '"hello"',
                (
                    '(json-parse-string "[1,2,3]" '
                    ":object-type 'alist :array-type 'list "
                    ":null-object nil :false-object :false)"
                ),
                "nil",
                "t",
                "nil",
                '"bar"',
            ],
        ),
    ],
)
def test_resolve_eval_request_maps_commands(
    argv: list[str], expected_func: str, expected_args: list[str]
) -> None:
    request = core.resolve_eval_request(parse_args(argv))

    assert request.func == expected_func
    assert request.arg_forms == expected_args


def test_decode_emacsclient_output_handles_quoted_base64() -> None:
    encoded = base64.b64encode("snowman ☃".encode()).decode("ascii")

    assert core.decode_emacsclient_output(f'"{encoded}"\n') == "snowman ☃"


def test_decode_emacsclient_output_handles_unquoted_base64() -> None:
    encoded = base64.b64encode(b"plain").decode("ascii")

    assert core.decode_emacsclient_output(f"{encoded}\n") == "plain"


def test_run_emacs_eval_includes_server_file(monkeypatch: pytest.MonkeyPatch) -> None:
    seen: dict[str, object] = {}

    def fake_run(
        cmd: list[str], capture_output: bool, text: bool
    ) -> subprocess.CompletedProcess[str]:
        seen["cmd"] = cmd
        seen["capture_output"] = capture_output
        seen["text"] = text
        encoded = base64.b64encode(b"ok").decode("ascii")
        return subprocess.CompletedProcess(cmd, 0, stdout=f'"{encoded}"\n', stderr="")

    monkeypatch.setattr(core.subprocess, "run", fake_run)

    result = core.run_emacs_eval('(message "hi")', "/tmp/emacs.sock")

    assert result == "ok"
    assert seen["cmd"] == [
        "emacsclient",
        "--server-file",
        "/tmp/emacs.sock",
        "-e",
        '(message "hi")',
    ]
    assert seen["capture_output"] is True
    assert seen["text"] is True


def test_run_emacs_eval_uses_stderr_and_exit_code_on_failure(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    def fake_run(
        cmd: list[str], capture_output: bool, text: bool
    ) -> subprocess.CompletedProcess[str]:
        return subprocess.CompletedProcess(cmd, 7, stdout="", stderr="boom\n")

    monkeypatch.setattr(core.subprocess, "run", fake_run)

    with pytest.raises(SystemExit) as exc_info:
        core.run_emacs_eval('(message "hi")', None)

    assert exc_info.value.code == 7
    assert capsys.readouterr().err == "boom\n"
