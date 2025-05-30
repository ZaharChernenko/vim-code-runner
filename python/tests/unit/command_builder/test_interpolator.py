from src.command_builder import TInterpolatorCommandBuilder
from src.file_info_extractor import IFileInfoExtractor
from src.project_info_extractor import IProjectInfoExtractor


def test_interpolator(project_info_extractor: IProjectInfoExtractor, file_info_extractor: IFileInfoExtractor):
    def _helper(pattern: str, file_path_abs: str, expected_result: str):
        assert (
            TInterpolatorCommandBuilder(pattern, project_info_extractor, file_info_extractor).build(file_path_abs)
            == expected_result
        )

    _helper("$dir", "/home/user/file.txt", "/home/user/")
    _helper("$dirWithoutTrailingSlash", "/home/user/file.txt", "/home/user")
    _helper("$dirWithoutTrailingSlash$dir", "/home/user/file.txt", "/home/user/home/user/")
    _helper("$dir$fileName", "/home/user/file.txt", "/home/user/file.txt")
    _helper("$dir$fileName", "/home/user/file", "/home/user/file")
    _helper("$fullFileName", "/home/user/file.txt", "/home/user/file.txt")
    _helper("$dir$fileNameWithoutExt", "/home/user/file", "/home/user/file")
    _helper("$dir$fileNameWithoutExt", "/home/user/file.txt", "/home/user/file")
    _helper("$dir$fileNameWithoutExt", "/home/user/file.txt.cpp", "/home/user/file")
    _helper("$dir$fileNameWithoutExt$fileExt", "/home/user/file.txt.cpp", "/home/user/file.txt.cpp")
