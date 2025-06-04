from src.command_builder import TInterpolatorCommandBuilder
from src.file_info_extractor import IFileInfoExtractor
from src.project_info_extractor import IProjectInfoExtractor


class THelper:
    def __init__(self, project_info_extractor: IProjectInfoExtractor, file_info_extractor: IFileInfoExtractor):
        self._project_info_extractor: IProjectInfoExtractor = project_info_extractor
        self._file_info_extractor: IFileInfoExtractor = file_info_extractor

    def __call__(self, pattern: str, file_path_abs: str, expected_result: str):
        builder: TInterpolatorCommandBuilder = TInterpolatorCommandBuilder(
            pattern, self._project_info_extractor, self._file_info_extractor
        )
        assert builder.build(file_path_abs) == expected_result


def test_interpolator_file_info_extractor(
    fixture_project_info_extractor: IProjectInfoExtractor, fixture_file_info_extractor: IFileInfoExtractor
):
    helper: THelper = THelper(fixture_project_info_extractor, fixture_file_info_extractor)
    helper("$dir", "/home/user/file.txt", "/home/user/")
    helper("$dirWithoutTrailingSlash", "/home/user/file.txt", "/home/user")
    helper("$dirWithoutTrailingSlash$dir", "/home/user/file.txt", "/home/user/home/user/")
    helper("$dir$fileName", "/home/user/file.txt", "/home/user/file.txt")
    helper("$dir$fileName", "/home/user/file", "/home/user/file")
    helper("$fullFileName", "/home/user/file.txt", "/home/user/file.txt")
    helper("$dir$fileNameWithoutExt", "/home/user/file", "/home/user/file")
    helper("$dir$fileNameWithoutExt", "/home/user/file.txt", "/home/user/file")
    helper("$dir$fileNameWithoutExt", "/home/user/file.txt.cpp", "/home/user/file")
    helper("$dir$fileNameWithoutExt$fileExt", "/home/user/file.txt.cpp", "/home/user/file.txt.cpp")


def test_interpolator_project_info_extractor(
    fixture_project_info_extractor: IProjectInfoExtractor, fixture_file_info_extractor: IFileInfoExtractor
):
    helper: THelper = THelper(fixture_project_info_extractor, fixture_file_info_extractor)
    workspace_root: str = fixture_project_info_extractor.get_workspace_root()

    helper("$workspaceRoot", "/home/user/file", workspace_root)
    helper("$workspaceRoot/$fileName", "/home/user/file.txt", f"{workspace_root}/file.txt")
    helper("$workspaceRoot/$fileNameWithoutExt", "/home/user/file", f"{workspace_root}/file")
