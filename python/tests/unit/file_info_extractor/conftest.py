import pytest

from src.file_info_extractor import IFileInfoExtractor, TBasicFileInfoExtractor


@pytest.fixture
def basic_file_info_extractor() -> TBasicFileInfoExtractor:
    return TBasicFileInfoExtractor()


@pytest.fixture(params=[pytest.param("basic_file_info_extractor")])
def file_info_extractor(request: pytest.FixtureRequest) -> IFileInfoExtractor:
    return request.getfixturevalue(request.param)
