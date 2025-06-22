import os
import tempfile
from unittest.mock import patch

import pytest

from src.file_info_extractor import IFileInfoExtractor


class TestFileInfoExtractorInterface:
    def test_get_dir(self, fixture_file_info_extractor: IFileInfoExtractor):
        assert fixture_file_info_extractor.get_dir("/home/user/project/file.py") == "/home/user/project/"
        assert fixture_file_info_extractor.get_dir("/home/file.txt") == "/home/"
        assert fixture_file_info_extractor.get_dir("/home/") == "/home/"
        assert fixture_file_info_extractor.get_dir("/home") == "/"
        assert fixture_file_info_extractor.get_dir("/file.txt") == "/"
        assert fixture_file_info_extractor.get_dir("/") == "/"

    def test_get_dir_without_trailing_slash(self, fixture_file_info_extractor: IFileInfoExtractor):
        assert fixture_file_info_extractor.get_dir_without_trailing_slash("/file.py") == ""
        assert (
            fixture_file_info_extractor.get_dir_without_trailing_slash("/home/user/project/file.py")
            == "/home/user/project"
        )

    def test_get_file_name(self, fixture_file_info_extractor: IFileInfoExtractor):
        assert fixture_file_info_extractor.get_file_name("/home/user/project/file.py") == "file.py"

    def test_get_file_name_without_ext(self, fixture_file_info_extractor: IFileInfoExtractor):
        assert fixture_file_info_extractor.get_file_name_without_ext("/home/user/project/file") == "file"
        assert fixture_file_info_extractor.get_file_name_without_ext("/home/user/project/file.py") == "file"
        assert fixture_file_info_extractor.get_file_name_without_ext("/home/user/project/file.tar.gz") == "file.tar"
        assert fixture_file_info_extractor.get_file_name_without_ext("/home/user/project/.zig.zon") == ".zig"

    def test_get_file_ext(self, fixture_file_info_extractor: IFileInfoExtractor):
        assert fixture_file_info_extractor.get_file_ext("/home/user/project/.zig.zon") == ".zon"
        assert fixture_file_info_extractor.get_file_ext("/home/user/project/file") == ""
        assert fixture_file_info_extractor.get_file_ext("/home/user/project/file.py") == ".py"
        assert fixture_file_info_extractor.get_file_ext("/home/user/project/file.cPp") == ".cpp"

    def test_get_file_type(self, fixture_file_info_extractor: IFileInfoExtractor):
        assert fixture_file_info_extractor.get_file_type("/home/user/project/file.py") == "python"
        assert fixture_file_info_extractor.get_file_type("/home/user/project/file.rs") == "rust"
        assert fixture_file_info_extractor.get_file_type("/home/user/project/file.cpp") == "cpp"
        assert fixture_file_info_extractor.get_file_type("/home/user/project/file.unknownext") is None
        assert fixture_file_info_extractor.get_file_type("/home/user/project/file.PY") == "python"

    def test_get_drive_letter_windows(self, fixture_file_info_extractor: IFileInfoExtractor):
        # On Unix, drive will be '', on Windows, 'C:'
        path = "C:\\Users\\user\\file.py"
        expected = os.path.splitdrive(path)[0]
        assert fixture_file_info_extractor.get_drive_letter(path) == expected

    def test_get_drive_letter_unix(self, fixture_file_info_extractor: IFileInfoExtractor):
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
    def test_get_shebang(self, fixture_file_info_extractor: IFileInfoExtractor, content, expected):
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

    def test_get_shebang_io_error_handling(self, fixture_file_info_extractor: IFileInfoExtractor):
        with patch("builtins.open", side_effect=IOError("Permission denied")):
            assert fixture_file_info_extractor.get_shebang("/some/file") is None

    def test_get_shebang_unicode_decode_error_handling(self, fixture_file_info_extractor: IFileInfoExtractor):
        with patch("builtins.open", side_effect=UnicodeDecodeError("utf-8", b"", 0, 1, "Invalid byte")):
            assert fixture_file_info_extractor.get_shebang("/some/file") is None
