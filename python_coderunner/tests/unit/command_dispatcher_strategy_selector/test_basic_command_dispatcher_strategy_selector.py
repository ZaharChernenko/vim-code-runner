from typing import List, Optional
from unittest.mock import MagicMock

import pytest

from src.command_builder import ICommandBuilder
from src.command_builders_dispatcher import (
    TFileExtCommandBuildersDispatcher,
    TFileTypeCommandBuildersDispatcher,
    TGlobCommandBuildersDispatcher,
    TShebangCommandBuildersDispatcher,
)
from src.command_dispatcher_strategy_selector import (
    TBasicCommandDispatcherStrategySelector,
)
from src.config_manager import EDispatchersTypes, TBasicConfigManager


@pytest.mark.parametrize(
    ("file_path", "content", "order", "respect_shebang", "expected"),
    [
        (
            "script.py",
            b"#!/usr/bin/python",
            [EDispatchersTypes.BY_GLOB, EDispatchersTypes.BY_FILE_EXT],
            True,
            "/usr/bin/python",
        ),
        (
            "script.sh",
            b"#!/usr/bin/bash",
            [EDispatchersTypes.BY_GLOB, EDispatchersTypes.BY_FILE_EXT],
            True,
            "/usr/bin/bash",
        ),
        (
            "script.rs",
            b"#![crate_type = 'lib']",
            [EDispatchersTypes.BY_FILE_EXT, EDispatchersTypes.BY_GLOB],
            True,
            None,
        ),
        (
            "script.py",
            b"#!/usr/bin/python",
            [EDispatchersTypes.BY_GLOB, EDispatchersTypes.BY_FILE_EXT, EDispatchersTypes.BY_FILE_TYPE],
            False,
            "**/*.py",
        ),
        (
            "script.py",
            b"#!/usr/bin/python",
            [EDispatchersTypes.BY_FILE_EXT, EDispatchersTypes.BY_GLOB, EDispatchersTypes.BY_FILE_TYPE],
            False,
            ".py",
        ),
        (
            "script.py",
            b"#!/usr/bin/python",
            [EDispatchersTypes.BY_FILE_TYPE, EDispatchersTypes.BY_GLOB, EDispatchersTypes.BY_FILE_EXT],
            False,
            "python",
        ),
    ],
)
def test_basic_command_dispatcher_strategy_selector(
    fixture_shebang_command_builders_dispatcher: TShebangCommandBuildersDispatcher,
    fixture_glob_command_builders_dispatcher: TGlobCommandBuildersDispatcher,
    fixture_file_ext_command_builders_dispatcher: TFileExtCommandBuildersDispatcher,
    fixture_file_type_command_builders_dispatcher: TFileTypeCommandBuildersDispatcher,
    file_path: str,
    content: bytes,
    order: List[EDispatchersTypes],
    respect_shebang: bool,
    expected: Optional[str],
    tmp_path,
):
    file_path_abs = tmp_path / file_path
    file_path_abs.write_bytes(content)
    config_manager: TBasicConfigManager = MagicMock(
        get_dispatchers_order=MagicMock(return_value=order), get_respect_shebang=MagicMock(return_value=respect_shebang)
    )
    selector = TBasicCommandDispatcherStrategySelector(
        shebang_command_builders_dispatcher=fixture_shebang_command_builders_dispatcher,
        glob_command_builders_dispatcher=fixture_glob_command_builders_dispatcher,
        file_ext_command_builders_dispatcher=fixture_file_ext_command_builders_dispatcher,
        file_type_command_builders_dispatcher=fixture_file_type_command_builders_dispatcher,
        config_manager=config_manager,
    )
    dispatch_result: Optional[ICommandBuilder] = selector.dispatch(str(file_path_abs))

    if expected is None:
        assert dispatch_result is None
    else:
        assert dispatch_result is not None
        if respect_shebang:
            assert dispatch_result.build(str(file_path_abs)) == f'{expected} "{str(file_path_abs)}"'
        else:
            assert dispatch_result.build(str(file_path_abs)) == expected
