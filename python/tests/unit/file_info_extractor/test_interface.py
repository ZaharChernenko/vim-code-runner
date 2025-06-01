import os

from src.file_info_extractor import TBasicFileInfoExtractor


def test_get_dir(file_info_extractor: TBasicFileInfoExtractor):
    assert file_info_extractor.get_dir("/home/user/project/file.py") == "/home/user/project/"
    assert file_info_extractor.get_dir("/home/file.txt") == "/home/"
    assert file_info_extractor.get_dir("/home/") == "/home/"
    assert file_info_extractor.get_dir("/home") == "/"
    assert file_info_extractor.get_dir("/file.txt") == "/"
    assert file_info_extractor.get_dir("/") == "/"


def test_get_dir_without_trailing_slash(file_info_extractor: TBasicFileInfoExtractor):
    assert file_info_extractor.get_dir_without_trailing_slash("/home/user/project/file.py") == "/home/user/project"
    assert file_info_extractor.get_dir_without_trailing_slash("/file.py") == ""


def test_get_file_name(file_info_extractor: TBasicFileInfoExtractor):
    assert file_info_extractor.get_file_name("/home/user/project/file.py") == "file.py"


def test_get_file_name_without_ext(file_info_extractor: TBasicFileInfoExtractor):
    assert file_info_extractor.get_file_name_without_ext("/home/user/project/file") == "file"
    assert file_info_extractor.get_file_name_without_ext("/home/user/project/file.py") == "file"
    assert file_info_extractor.get_file_name_without_ext("/home/user/project/file.tar.gz") == "file"
    assert file_info_extractor.get_file_name_without_ext("/home/user/project/.zig.zon") == ""


def test_get_file_ext(file_info_extractor: TBasicFileInfoExtractor):
    assert file_info_extractor.get_file_ext("/home/user/project/.zig.zon") == ".zig.zon"
    assert file_info_extractor.get_file_ext("/home/user/project/file") == ""
    assert file_info_extractor.get_file_ext("/home/user/project/file.py") == ".py"
    assert file_info_extractor.get_file_ext("/home/user/project/file.cPp") == ".cpp"


def test_get_file_type(file_info_extractor: TBasicFileInfoExtractor):
    assert file_info_extractor.get_file_type("/home/user/project/file.py") == "Python"
    assert file_info_extractor.get_file_type("/home/user/project/file.rs") == "Rust"
    assert file_info_extractor.get_file_type("/home/user/project/file.cpp") == "C++"
    assert file_info_extractor.get_file_type("/home/user/project/file.unknownext") is None
    assert file_info_extractor.get_file_type("/home/user/project/file.PY") == "Python"
    assert file_info_extractor.get_file_type("/home/user/project/file.axs.erb") == "NetLinx+ERB"
    assert file_info_extractor.get_file_type("/home/user/project/.zig.zon") == "Zig"


def test_get_full_file_name(file_info_extractor: TBasicFileInfoExtractor):
    assert file_info_extractor.get_full_file_name("/home/user/project/file.py") == "/home/user/project/file.py"
    assert file_info_extractor.get_full_file_name("/home/user/project/.zig.zon") == "/home/user/project/.zig.zon"
    assert file_info_extractor.get_full_file_name("/home/user/file.unknown") == "/home/user/file.unknown"


def test_get_drive_letter_windows(file_info_extractor: TBasicFileInfoExtractor):
    # On Unix, drive will be '', on Windows, 'C:'
    path = "C:\\Users\\user\\file.py"
    expected = os.path.splitdrive(path)[0]
    assert file_info_extractor.get_drive_letter(path) == expected


def test_get_drive_letter_unix(file_info_extractor: TBasicFileInfoExtractor):
    path = "/home/user/file.py"
    assert file_info_extractor.get_drive_letter(path) == ""
