from typing import Optional

import pytest

from src.command_builder import ICommandBuilder
from src.command_builders_dispatcher import TFileTypeCommandBuildersDispatcher


@pytest.mark.parametrize(
    ("file_path", "expected_build_result"),
    [
        ("/home/script.py", "**/*.py"),
        ("/home/.ycm.py", "**/*.py"),
        (".ycm.py", "**/*.py"),
        ("file.js", "*.js"),
        ("file.8xp.txt", "*.8xp.txt"),
        ("x.y.z", "*.*.*"),
        ("/home/usr/x.y.z", "**/*.*.*"),
    ],
)
def test_glob_command_builders_dispatcher(
    fixture_glob_command_builders_dispatcher: TFileTypeCommandBuildersDispatcher,
    file_path: str,
    expected_build_result: Optional[str],
):
    dispatch_result: Optional[ICommandBuilder] = fixture_glob_command_builders_dispatcher.dispatch(file_path)

    if expected_build_result is not None:
        assert dispatch_result is not None
        assert dispatch_result.build(file_path) == expected_build_result
    else:
        assert dispatch_result is None
