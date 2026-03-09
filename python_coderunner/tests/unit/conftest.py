import glob
import re
import sys
import tempfile
import unittest
from typing import Dict, Generator, Tuple
from unittest import mock
from unittest.mock import MagicMock

import pytest
from pytest_lazyfixture import lazy_fixture

sys.modules["vim"] = MagicMock()
from src.command_builder import ICommandBuilder
from src.command_builders_dispatcher import (
    TFileExtCommandBuildersDispatcher,
    TFileTypeCommandBuildersDispatcher,
    TGlobCommandBuildersDispatcher,
    TShebangCommandBuildersDispatcher,
)
from src.config_manager import (
    ConfigField,
    EDispatchersTypes,
    IConfigGetter,
    IConfigManager,
    TVimConfigGetter,
    TVimConfigManager,
)
from src.file_info_extractor import (
    IFileInfoExtractor,
    TVimFileInfoExtractor,
)
from src.project_info_extractor import (
    IProjectInfoExtractor,
    TVimProjectInfoExtractor,
)
from src.validators import TBoolValidator, TDispatchersOrderValidator, TDispatchersValidator, TStrValidator


@pytest.fixture(params=(lazy_fixture("fixture_vim_config_manager"),))
def fixture_config_manager(request: pytest.FixtureRequest) -> IConfigManager:
    return request.param


@pytest.fixture
def fixture_vim_config_manager(fixture_config_getter: IConfigGetter) -> IConfigManager:
    """Create TVimConfigManager with all ConfigField objects"""
    return TVimConfigManager(
        by_file_ext_field=ConfigField(
            name="by_file_ext",
            getter=fixture_config_getter.get_by_file_ext,
            validator=TDispatchersValidator(),
            allowed_values_description="Dict[str, str] value",
        ),
        by_file_type_field=ConfigField(
            name="by_file_type",
            getter=fixture_config_getter.get_by_file_type,
            validator=TDispatchersValidator(),
            allowed_values_description="Dict[str, str] value",
        ),
        by_glob_field=ConfigField(
            name="by_glob",
            getter=fixture_config_getter.get_by_glob,
            validator=TDispatchersValidator(),
            allowed_values_description="Dict[str, str] value",
        ),
        dispatchers_order_field=ConfigField(
            name="runners_order",
            getter=fixture_config_getter.get_dispatchers_order,
            validator=TDispatchersOrderValidator(set(EDispatchersTypes)),
            allowed_values_description=", ".join(dispatcher_type.value for dispatcher_type in EDispatchersTypes),
        ),
        coderunner_tempfile_prefix_field=ConfigField(
            name="coderunner_tempfile_prefix",
            getter=fixture_config_getter.get_coderunner_tempfile_prefix,
            validator=TStrValidator(),
            allowed_values_description="str value",
        ),
        executor_field=ConfigField(
            name="executor",
            getter=fixture_config_getter.get_executor,
            validator=TStrValidator(),
            allowed_values_description="str value",
        ),
        ignore_selection_field=ConfigField(
            name="ignore_selection",
            getter=fixture_config_getter.get_ignore_selection,
            validator=TBoolValidator(),
            allowed_values_description="0 or 1",
        ),
        respect_shebang_field=ConfigField(
            name="respect_shebang",
            getter=fixture_config_getter.get_respect_shebang,
            validator=TBoolValidator(),
            allowed_values_description="0 or 1",
        ),
        remove_coderunner_tempfiles_on_exit_field=ConfigField(
            name="coderunner_remove_coderunner_tempfiles_on_exit",
            getter=fixture_config_getter.get_remove_coderunner_tempfiles_on_exit,
            validator=TBoolValidator(),
            allowed_values_description="0 or 1",
        ),
        save_all_files_before_run_field=ConfigField(
            name="save_all_files_before_run",
            getter=fixture_config_getter.get_save_all_files_before_run,
            validator=TBoolValidator(),
            allowed_values_description="0 or 1",
        ),
        save_file_before_run_field=ConfigField(
            name="save_file_before_run",
            getter=fixture_config_getter.get_save_file_before_run,
            validator=TBoolValidator(),
            allowed_values_description="0 or 1",
        ),
    )


@pytest.fixture(params=(lazy_fixture("fixture_vim_config_getter"),))
def fixture_config_getter(request: pytest.FixtureRequest) -> IConfigGetter:
    return request.param


@pytest.fixture
def fixture_vim_config_getter() -> IConfigGetter:
    return TVimConfigGetter()


@pytest.fixture
def fixture_shebang_command_builders_dispatcher(
    fixture_file_info_extractor: IFileInfoExtractor,
) -> TShebangCommandBuildersDispatcher:
    return TShebangCommandBuildersDispatcher(fixture_file_info_extractor)


@pytest.fixture
def fixture_file_ext_command_builders_dispatcher(
    fixture_file_info_extractor: IFileInfoExtractor,
) -> TFileExtCommandBuildersDispatcher:
    extensions: Tuple[str, ...] = (".py", ".js", ".ts", ".java", ".cpp", ".c", ".go", ".rb", ".txt", ".z")
    file_ext_to_builder: Dict[str, ICommandBuilder] = {
        ext: MagicMock(spec=ICommandBuilder, build=MagicMock(return_value=ext)) for ext in extensions
    }

    return TFileExtCommandBuildersDispatcher(
        file_ext_to_builder=file_ext_to_builder, file_info_extractor=fixture_file_info_extractor
    )


@pytest.fixture
def fixture_file_type_command_builders_dispatcher(
    fixture_file_info_extractor: IFileInfoExtractor,
) -> TFileTypeCommandBuildersDispatcher:
    languages: Tuple[str, ...] = (
        "python",
        "javascript",
        "typescript",
        "cpp",
    )
    file_type_to_builder: Dict[str, ICommandBuilder] = {
        lang: MagicMock(spec=ICommandBuilder, build=MagicMock(return_value=lang)) for lang in languages
    }

    return TFileTypeCommandBuildersDispatcher(
        file_type_to_builder=file_type_to_builder, file_info_extractor=fixture_file_info_extractor
    )


@pytest.fixture
def fixture_glob_command_builders_dispatcher() -> TGlobCommandBuildersDispatcher:
    glob_patterns: Tuple[str, ...] = (
        "**/*.py",
        "**/test.py",
        "*.js",
        "*.java",
        "*.cpp",
        "*.8xp.txt",
        "*.*.*",
        "**/*.log",
        "**/*.*.*",
    )
    glob_to_builder: Tuple[Tuple[re.Pattern, ICommandBuilder], ...] = tuple(
        (
            re.compile(glob.translate(pattern, recursive=True, include_hidden=True)),
            MagicMock(spec=ICommandBuilder, build=MagicMock(return_value=pattern)),
        )
        for pattern in sorted(glob_patterns, reverse=True)
    )

    return TGlobCommandBuildersDispatcher(glob_to_builder)


@pytest.fixture(params=(lazy_fixture("fixture_vim_project_info_extractor"),))
def fixture_project_info_extractor(request: pytest.FixtureRequest) -> IProjectInfoExtractor:
    return request.param


@pytest.fixture
def fixture_vim_project_info_extractor(
    fixture_file_info_extractor: IFileInfoExtractor,
) -> Generator[IProjectInfoExtractor, None, None]:
    with tempfile.TemporaryDirectory() as temp_dir:
        extractor: TVimProjectInfoExtractor = TVimProjectInfoExtractor(fixture_file_info_extractor)
        with mock.patch.object(
            extractor,
            "get_workspace_root",
            return_value=temp_dir,
        ):
            yield extractor


@pytest.fixture(params=(lazy_fixture("fixture_vim_file_info_extractor"),))
def fixture_file_info_extractor(request: pytest.FixtureRequest) -> IFileInfoExtractor:
    return request.param


@pytest.fixture
def fixture_vim_file_info_extractor() -> Generator[IFileInfoExtractor, None, None]:
    extractor: TVimFileInfoExtractor = TVimFileInfoExtractor()
    ext_to_lang: Dict[str, str] = {
        ".py": "python",
        ".cpp": "cpp",
        ".rs": "rust",
        ".ts": "typescript",
        ".js": "javascript",
    }
    with mock.patch.object(
        extractor,
        "get_file_type",
        side_effect=lambda file_path_abs: ext_to_lang.get(extractor.get_file_ext(file_path_abs)),
    ):
        yield extractor
