import glob
import re
import sys
import tempfile
import unittest
from typing import Dict, Generator, Tuple
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
    IConfigGetter,
    TBasicConfigManager,
    TBasicConfigValidator,
    TVimConfigGetter,
    TVimConfigManager,
)
from src.file_info_extractor import IFileInfoExtractor, TVimFileInfoExtractor
from src.project_info_extractor import IProjectInfoExtractor, TVimProjectInfoExtractor


@pytest.fixture(params=(lazy_fixture("fixture_vim_config_manager"),))
def fixture_config_manager(request: pytest.FixtureRequest) -> TBasicConfigManager:
    return request.param


@pytest.fixture
def fixture_vim_config_manager(
    fixture_config_getter: IConfigGetter, fixture_config_validator: TBasicConfigValidator
) -> TBasicConfigManager:
    return TVimConfigManager(fixture_config_getter, fixture_config_validator)


@pytest.fixture(params=(lazy_fixture("fixture_vim_config_getter"),))
def fixture_config_getter(request: pytest.FixtureRequest) -> IConfigGetter:
    return request.param


@pytest.fixture
def fixture_vim_config_getter() -> IConfigGetter:
    return TVimConfigGetter()


@pytest.fixture(params=(lazy_fixture("fixture_basic_config_validator"),))
def fixture_config_validator(request: pytest.FixtureRequest) -> TBasicConfigValidator:
    return request.param


@pytest.fixture
def fixture_basic_config_validator() -> TBasicConfigValidator:
    return TBasicConfigValidator()


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
) -> Generator[IProjectInfoExtractor]:
    with tempfile.TemporaryDirectory() as temp_dir:
        extractor: TVimProjectInfoExtractor = TVimProjectInfoExtractor(fixture_file_info_extractor)
        with unittest.mock.patch.object(
            extractor,
            "get_workspace_root",
            return_value=temp_dir,
        ):
            yield extractor


@pytest.fixture(params=(lazy_fixture("fixture_vim_file_info_extractor"),))
def fixture_file_info_extractor(request: pytest.FixtureRequest) -> IFileInfoExtractor:
    return request.param


@pytest.fixture
def fixture_vim_file_info_extractor() -> Generator[IFileInfoExtractor]:
    extractor: TVimFileInfoExtractor = TVimFileInfoExtractor()
    ext_to_lang: Dict[str, str] = {
        ".py": "python",
        ".cpp": "cpp",
        ".rs": "rust",
        ".ts": "typescript",
        ".js": "javascript",
    }
    with unittest.mock.patch.object(
        extractor,
        "get_file_type",
        side_effect=lambda file_path_abs: ext_to_lang.get(extractor.get_file_ext(file_path_abs)),
    ):
        yield extractor
