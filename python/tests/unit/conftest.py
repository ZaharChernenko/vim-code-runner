import glob
import re
import sys
import tempfile
import unittest
from typing import Callable, Dict, Generator, List, Sequence, Tuple
from unittest.mock import MagicMock

import pytest
import pytest_mock

sys.modules["vim"] = MagicMock()
from src.command_builder import ICommandBuilder
from src.command_builders_dispatcher import (
    TFileExtCommandBuildersDispatcher,
    TFileTypeCommandBuildersDispatcher,
    TGlobCommandBuildersDispatcher,
    TShebangCommandBuildersDispatcher,
)
from src.config_manager import IConfigManager, TVimConfigManager
from src.file_info_extractor import IFileInfoExtractor, TBasicFileInfoExtractor
from src.project_info_extractor import IProjectInfoExtractor, TVimProjectInfoExtractor


def vim_config_manager_extractor_factory() -> Generator[IConfigManager]:
    yield TVimConfigManager()


def get_all_config_managers_factories() -> Sequence[Callable[..., Generator[IConfigManager]]]:
    return (vim_config_manager_extractor_factory,)


@pytest.fixture(params=get_all_config_managers_factories())
def fixture_config_manager(request: pytest.FixtureRequest) -> Generator[IConfigManager]:
    yield from request.param()


def vim_project_info_extractor_factory(file_info_extractor: IFileInfoExtractor) -> Generator[IProjectInfoExtractor]:
    with tempfile.TemporaryDirectory() as temp_dir:
        extractor = TVimProjectInfoExtractor(file_info_extractor)
        with unittest.mock.patch.object(
            extractor,
            "get_workspace_root",
            return_value=temp_dir,
        ):
            yield extractor


def get_all_project_info_extractors_factories(
    file_info_extractors_factories: Sequence[Callable[[], IFileInfoExtractor]],
) -> Sequence[Callable[..., Generator[IProjectInfoExtractor]]]:
    """
    The problem is that the params in the fixture are defined only once, so if you use the fixture
    more than once, all the generators inside are invalidated, so you need to create a generator factory.
    """
    project_info_extractors_factories: list[Callable[..., Generator[IProjectInfoExtractor]]] = []
    for file_info_extractor_factory in file_info_extractors_factories:
        project_info_extractors_factories.append(
            lambda file_info_extractor_factory=file_info_extractor_factory: vim_project_info_extractor_factory(
                file_info_extractor_factory()
            )
        )

    return project_info_extractors_factories


def get_all_file_info_extractors_factories() -> Sequence[Callable[[], IFileInfoExtractor]]:
    return (TBasicFileInfoExtractor,)


@pytest.fixture
def fixture_shebang_command_builders_dispatcher(
    fixture_file_info_extractor: IFileInfoExtractor,
) -> TShebangCommandBuildersDispatcher:
    return TShebangCommandBuildersDispatcher(fixture_file_info_extractor)


@pytest.fixture
def fixture_glob_command_builders_dispatcher() -> TGlobCommandBuildersDispatcher:
    glob_patterns = ("**/*.py", "*.js", "*.java", "*.cpp", "*.8xp.txt", "*.*.*", "**/*.log", "**/*.*.*")
    glob_to_builder: Tuple[Tuple[re.Pattern, ICommandBuilder], ...] = tuple(
        (
            re.compile(glob.translate(pattern, recursive=True, include_hidden=True)),
            MagicMock(spec=ICommandBuilder, build=MagicMock(return_value=pattern)),
        )
        for pattern in glob_patterns
    )

    return TGlobCommandBuildersDispatcher(glob_to_builder)


@pytest.fixture
def fixture_file_ext_command_builders_dispatcher(
    fixture_file_info_extractor: IFileInfoExtractor,
) -> TFileExtCommandBuildersDispatcher:
    extensions: List[str] = [".py", ".js", ".ts", ".java", ".cpp", ".c", ".go", ".rb", ".8xp.txt", ".x.y.z"]
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
    languages: List[str] = ["Python", "JavaScript", "TypeScript", "Java", "C++", "C", "Go", "Ruby", "PHP", "Shell"]
    file_type_to_builder: Dict[str, ICommandBuilder] = {
        lang: MagicMock(spec=ICommandBuilder, build=MagicMock(return_value=lang)) for lang in languages
    }

    return TFileTypeCommandBuildersDispatcher(
        file_type_to_builder=file_type_to_builder, file_info_extractor=fixture_file_info_extractor
    )


@pytest.fixture(params=get_all_project_info_extractors_factories(get_all_file_info_extractors_factories()))
def fixture_project_info_extractor(request: pytest.FixtureRequest) -> Generator[IFileInfoExtractor]:
    yield from request.param()


@pytest.fixture(params=get_all_file_info_extractors_factories())
def fixture_file_info_extractor(request: pytest.FixtureRequest) -> IFileInfoExtractor:
    return request.param()
