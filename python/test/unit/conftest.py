import sys
import tempfile
import unittest
from typing import Callable, Generator, Sequence
from unittest.mock import MagicMock

import pytest

sys.modules["vim"] = MagicMock()
from src.command_builders_dispatcher import TShebangCommandBuildersDispatcher
from src.file_info_extractor import IFileInfoExtractor, TBasicFileInfoExtractor
from src.project_info_extractor import IProjectInfoExtractor, TVimProjectInfoExtractor


def vim_project_info_extractor_factory(file_info_extractor: IFileInfoExtractor) -> Generator[IProjectInfoExtractor]:
    with tempfile.TemporaryDirectory() as temp_dir:
        extractor = TVimProjectInfoExtractor(file_info_extractor)
        unittest.mock.patch.object(
            extractor,
            "get_workspace_root",
            return_value=temp_dir,
        ).start()

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


@pytest.fixture(params=get_all_project_info_extractors_factories(get_all_file_info_extractors_factories()))
def fixture_project_info_extractor(request: pytest.FixtureRequest) -> Generator[IFileInfoExtractor]:
    yield from request.param()


@pytest.fixture(params=get_all_file_info_extractors_factories())
def fixture_file_info_extractor(request: pytest.FixtureRequest) -> IFileInfoExtractor:
    return request.param()
