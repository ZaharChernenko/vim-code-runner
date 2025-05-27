import tempfile

import pytest

from src.file_info_extractor import IFileInfoExtractor
from src.project_info_extractor import IProjectInfoExtractor, TVimProjectInfoExtractor
from tests.unit.file_info_extractor.conftest import (
    basic_file_info_extractor,
    file_info_extractor,
)


@pytest.fixture
def vim_project_info_extractor(mocker, file_info_extractor: IFileInfoExtractor):
    with tempfile.TemporaryDirectory() as temp_dir:
        extractor = TVimProjectInfoExtractor(file_info_extractor)
        mocker.patch.object(
            extractor,
            "get_workspace_root",
            return_value=temp_dir,
        )

        yield extractor


@pytest.fixture(params=[pytest.param("vim_project_info_extractor")])
def project_info_extractor(request: pytest.FixtureRequest) -> IProjectInfoExtractor:
    return request.getfixturevalue(request.param)
