from typing import Optional

import pytest

from src.command_builder import TConcatenatorCommandBuilder


@pytest.mark.parametrize(
    ("content", "expected_result"),
    [
        pytest.param(None, None, id="nonexistent file"),
        pytest.param(b"print('Hello')", None, id="no shebang"),
        pytest.param(b"\n\ncode", None, id="empty first line"),
        pytest.param(b"#![feature(test)]", None, id="Rust attribute"),
        pytest.param(b"#!/bin/bash", "/bin/bash", id="basic shebang"),
        pytest.param(b"#!/usr/bin/env python", "/usr/bin/env python", id="env shebang"),
        pytest.param(b"  #!/bin/sh  ", "/bin/sh", id="whitespace around shebang"),
        pytest.param(b"#!", "", id="empty shebang"),
        pytest.param(b"#!\ncode", "", id="shebang with no path"),
        pytest.param(b"#!/usr/bin/python", "/usr/bin/python", id="shebang without newline"),
        pytest.param(b"#!/bin/bash -x\ndef f():\n\treturn0", "/bin/bash -x", id="shebang with multiple lines"),
    ],
)
def test_shebang_command_builders_dispatcher(
    fixture_shebang_command_builders_dispatcher, content, expected_result, tmp_path
):
    file_path_abs = tmp_path / "test_file"

    if content is None:
        assert fixture_shebang_command_builders_dispatcher.dispatch(str(file_path_abs)) is None
        return

    file_path_abs.write_bytes(content)
    dispatch_result: Optional[TConcatenatorCommandBuilder] = fixture_shebang_command_builders_dispatcher.dispatch(
        file_path_abs
    )

    if expected_result is None:
        assert dispatch_result is None
    else:
        assert dispatch_result is not None
        assert dispatch_result.build(str(file_path_abs)) == f"{expected_result} '{file_path_abs}'"
