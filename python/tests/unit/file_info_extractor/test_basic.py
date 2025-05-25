import os

import pytest

from src.file_info_extractor import TBasicFileInfoExtractor


@pytest.fixture
def extractor():
    return TBasicFileInfoExtractor()


def test_get_workspace_root(extractor):
    assert extractor.get_workspace_root("/home/user/project/file.py") == "/home/user/project"


def test_get_dir(extractor):
    assert extractor.get_dir("/home/user/project/file.py") == "/home/user/project"


def test_get_dir_without_trailing_slash(extractor):
    assert extractor.get_dir_without_trailing_slash("/home/user/project/file.py") == "/home/user/project"
    assert extractor.get_dir_without_trailing_slash("/file.py") == ""


def test_get_file_name(extractor):
    assert extractor.get_file_name("/home/user/project/file.py") == "file.py"


def test_get_file_name_without_ext(extractor):
    assert extractor.get_file_name_without_ext("/home/user/project/file") == "file"
    assert extractor.get_file_name_without_ext("/home/user/project/file.py") == "file"
    assert extractor.get_file_name_without_ext("/home/user/project/file.tar.gz") == "file"
    assert extractor.get_file_name_without_ext("/home/user/project/.zig.zon") == ""


def test_get_file_type(extractor):
    assert extractor.get_file_type("/home/user/project/file.py") == "Python"
    assert extractor.get_file_type("/home/user/project/file.rs") == "Rust"
    assert extractor.get_file_type("/home/user/project/file.cpp") == "C++"
    assert extractor.get_file_type("/home/user/project/file.unknownext") is None
    assert extractor.get_file_type("/home/user/project/file.PY") == "Python"
    assert extractor.get_file_type("/home/user/project/file.axs.erb") == "NetLinx+ERB"
    assert extractor.get_file_type("/home/user/project/.zig.zon") == "Zig"


def test_get_drive_letter_windows(extractor):
    # On Unix, drive will be '', on Windows, 'C:'
    path = "C:\\Users\\user\\file.py"
    expected = os.path.splitdrive(path)[0]
    assert extractor.get_drive_letter(path) == expected


def test_get_drive_letter_unix(extractor):
    path = "/home/user/file.py"
    assert extractor.get_drive_letter(path) == ""
