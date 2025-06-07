import os
import tempfile
from unittest.mock import patch

import pytest

from src.file_info_extractor import TBasicFileInfoExtractor


def test_get_dir(fixture_file_info_extractor: TBasicFileInfoExtractor):
    assert fixture_file_info_extractor.get_dir("/home/user/project/file.py") == "/home/user/project/"
    assert fixture_file_info_extractor.get_dir("/home/file.txt") == "/home/"
    assert fixture_file_info_extractor.get_dir("/home/") == "/home/"
    assert fixture_file_info_extractor.get_dir("/home") == "/"
    assert fixture_file_info_extractor.get_dir("/file.txt") == "/"
    assert fixture_file_info_extractor.get_dir("/") == "/"


def test_get_dir_without_trailing_slash(fixture_file_info_extractor: TBasicFileInfoExtractor):
    assert fixture_file_info_extractor.get_dir_without_trailing_slash("/file.py") == ""
    assert (
        fixture_file_info_extractor.get_dir_without_trailing_slash("/home/user/project/file.py") == "/home/user/project"
    )


def test_get_file_name(fixture_file_info_extractor: TBasicFileInfoExtractor):
    assert fixture_file_info_extractor.get_file_name("/home/user/project/file.py") == "file.py"


def test_get_file_name_without_ext(fixture_file_info_extractor: TBasicFileInfoExtractor):
    assert fixture_file_info_extractor.get_file_name_without_ext("/home/user/project/file") == "file"
    assert fixture_file_info_extractor.get_file_name_without_ext("/home/user/project/file.py") == "file"
    assert fixture_file_info_extractor.get_file_name_without_ext("/home/user/project/file.tar.gz") == "file"
    assert fixture_file_info_extractor.get_file_name_without_ext("/home/user/project/.zig.zon") == ""


def test_get_file_ext(fixture_file_info_extractor: TBasicFileInfoExtractor):
    assert fixture_file_info_extractor.get_file_ext("/home/user/project/.zig.zon") == ".zig.zon"
    assert fixture_file_info_extractor.get_file_ext("/home/user/project/file") == ""
    assert fixture_file_info_extractor.get_file_ext("/home/user/project/file.py") == ".py"
    assert fixture_file_info_extractor.get_file_ext("/home/user/project/file.cPp") == ".cpp"


def test_get_file_type(fixture_file_info_extractor: TBasicFileInfoExtractor):
    assert fixture_file_info_extractor.get_file_type("/home/user/project/file.py") == "Python"
    assert fixture_file_info_extractor.get_file_type("/home/user/project/file.rs") == "Rust"
    assert fixture_file_info_extractor.get_file_type("/home/user/project/file.cpp") == "C++"
    assert fixture_file_info_extractor.get_file_type("/home/user/project/file.unknownext") is None
    assert fixture_file_info_extractor.get_file_type("/home/user/project/file.PY") == "Python"
    assert fixture_file_info_extractor.get_file_type("/home/user/project/file.axs.erb") == "NetLinx+ERB"
    assert fixture_file_info_extractor.get_file_type("/home/user/project/.zig.zon") == "Zig"


def test_get_full_file_name(fixture_file_info_extractor: TBasicFileInfoExtractor):
    assert fixture_file_info_extractor.get_full_file_name("/home/user/project/file.py") == "/home/user/project/file.py"
    assert fixture_file_info_extractor.get_full_file_name("/home/user/file.unknown") == "/home/user/file.unknown"
    assert (
        fixture_file_info_extractor.get_full_file_name("/home/user/project/.zig.zon") == "/home/user/project/.zig.zon"
    )


def test_get_drive_letter_windows(fixture_file_info_extractor: TBasicFileInfoExtractor):
    # On Unix, drive will be '', on Windows, 'C:'
    path = "C:\\Users\\user\\file.py"
    expected = os.path.splitdrive(path)[0]
    assert fixture_file_info_extractor.get_drive_letter(path) == expected


def test_get_drive_letter_unix(fixture_file_info_extractor: TBasicFileInfoExtractor):
    path = "/home/user/file.py"
    assert fixture_file_info_extractor.get_drive_letter(path) == ""


@pytest.mark.parametrize(
    ("content", "expected"),
    [
        pytest.param(None, None, id="nonexistent file"),
        pytest.param("print('Hello')", None, id="no shebang"),
        pytest.param("\n\ncode", None, id="empty first line"),
        pytest.param("#!/bin/bash", "/bin/bash", id="basic shebang"),
        pytest.param("#!/usr/bin/env python", "/usr/bin/env python", id="env shebang"),
        pytest.param("  #!/bin/sh  ", "/bin/sh", id="whitespace around shebang"),
        pytest.param("#![feature(test)]", None, id="Rust attribute"),
        pytest.param("#!", "", id="empty shebang"),
        pytest.param("#!\ncode", "", id="shebang with no path"),
        pytest.param("#!/usr/bin/python", "/usr/bin/python", id="shebang without newline"),
        pytest.param("#!/bin/bash -x\ndef f():\n\treturn0", "/bin/bash -x", id="shebang with multiple lines"),
    ],
)
def test_get_shebang(fixture_file_info_extractor, content, expected):
    if content is None:
        assert fixture_file_info_extractor.get_shebang("/bad/path") is expected
        return

    with tempfile.NamedTemporaryFile(mode="w", delete=False) as temp_file:
        temp_file.write(content)
        file_path = temp_file.name
    try:
        assert fixture_file_info_extractor.get_shebang(file_path) == expected
    finally:
        os.unlink(file_path)


def test_get_shebang_io_error_handling(fixture_file_info_extractor: TBasicFileInfoExtractor):
    with patch("builtins.open", side_effect=IOError("Permission denied")):
        assert fixture_file_info_extractor.get_shebang("/some/file") is None


def test_get_shebang_unicode_decode_error_handling(fixture_file_info_extractor: TBasicFileInfoExtractor):
    with patch("builtins.open", side_effect=UnicodeDecodeError("utf-8", b"", 0, 1, "Invalid byte")):
        assert fixture_file_info_extractor.get_shebang("/some/file") is None
