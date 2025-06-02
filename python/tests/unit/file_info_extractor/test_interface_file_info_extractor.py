import os

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
