import os
import tempfile
from typing import Optional

import pytest

from src.command_builder import TConcatenatorCommandBuilder


@pytest.mark.parametrize(
    ("content"),
    [
        pytest.param(None, id="nonexistent file"),
        pytest.param("print('Hello')", id="no shebang"),
        pytest.param("\n\ncode", id="empty first line"),
        pytest.param("#![feature(test)]", id="Rust attribute"),
    ],
)
def test_shebang_command_builders_dispatcher_empty(fixture_shebang_command_builders_dispatcher, content):
    if content is None:
        assert fixture_shebang_command_builders_dispatcher.dispatch("/bad/path") is None
        return

    with tempfile.NamedTemporaryFile(mode="w", delete=False) as temp_file:
        temp_file.write(content)
        file_path = temp_file.name
    try:
        assert fixture_shebang_command_builders_dispatcher.dispatch(file_path) is None
    finally:
        os.unlink(file_path)


@pytest.mark.parametrize(
    ("content", "expected_build_result"),
    [
        pytest.param("#!/bin/bash", "/bin/bash", id="basic shebang"),
        pytest.param("#!/usr/bin/env python", "/usr/bin/env python", id="env shebang"),
        pytest.param("  #!/bin/sh  ", "/bin/sh", id="whitespace around shebang"),
        pytest.param("#!", "", id="empty shebang"),
        pytest.param("#!\ncode", "", id="shebang with no path"),
        pytest.param("#!/usr/bin/python", "/usr/bin/python", id="shebang without newline"),
        pytest.param("#!/bin/bash -x\ndef f():\n\treturn0", "/bin/bash -x", id="shebang with multiple lines"),
    ],
)
def test_shebang_command_builders_dispatcher_non_empty(
    fixture_shebang_command_builders_dispatcher, content, expected_build_result
):
    with tempfile.NamedTemporaryFile(mode="w", delete=False) as temp_file:
        temp_file.write(content)
        file_path = temp_file.name
    try:
        builder: Optional[TConcatenatorCommandBuilder] = fixture_shebang_command_builders_dispatcher.dispatch(file_path)
        assert builder is not None
        assert builder.build(file_path) == f"{expected_build_result} '{file_path}'"
    finally:
        os.unlink(file_path)
