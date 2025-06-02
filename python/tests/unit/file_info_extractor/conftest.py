from typing import Callable, Sequence

import pytest

from src.file_info_extractor import IFileInfoExtractor, TBasicFileInfoExtractor


def get_all_file_info_extractors_factories() -> Sequence[Callable[[], IFileInfoExtractor]]:
    return (lambda: TBasicFileInfoExtractor(),)


@pytest.fixture(params=get_all_file_info_extractors_factories())
def fixture_file_info_extractor(request: pytest.FixtureRequest) -> IFileInfoExtractor:
    return request.param()
