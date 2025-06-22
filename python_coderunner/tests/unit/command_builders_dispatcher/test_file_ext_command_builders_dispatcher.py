from typing import Optional

import pytest

from src.command_builder import ICommandBuilder
from src.command_builders_dispatcher import TFileExtCommandBuildersDispatcher


@pytest.mark.parametrize(
    ("file_path", "expected_build_result"),
    [
        ("/home/script.py", ".py"),
        ("/app.js", ".js"),
        (".8xp.txt", ".txt"),
        ("/home/unknown.x.y.z", ".z"),
        ("/home/unknown.unknown", None),
    ],
)
def test_file_ext_command_builders_dispatcher(
    fixture_file_ext_command_builders_dispatcher: TFileExtCommandBuildersDispatcher,
    file_path: str,
    expected_build_result: Optional[str],
):
    dispatch_result: Optional[ICommandBuilder] = fixture_file_ext_command_builders_dispatcher.dispatch(file_path)

    if expected_build_result is not None:
        assert dispatch_result is not None
        assert dispatch_result.build(file_path) == expected_build_result
    else:
        assert dispatch_result is None
