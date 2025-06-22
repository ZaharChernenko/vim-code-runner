from src.command_builder import TInterpolatorCommandBuilder
from src.file_info_extractor import IFileInfoExtractor
from src.project_info_extractor import IProjectInfoExtractor


class TestInterpolatorCommandBuilder:
    def test_build(
        self, fixture_project_info_extractor: IProjectInfoExtractor, fixture_file_info_extractor: IFileInfoExtractor
    ):
        comparator: TestInterpolatorCommandBuilder.TComparator = TestInterpolatorCommandBuilder.TComparator(
            fixture_project_info_extractor, fixture_file_info_extractor
        )
        workspace_root: str = fixture_project_info_extractor.get_workspace_root()
        comparator("$dir", "/home/user/file.txt", "/home/user/")
        comparator("$dirWithoutTrailingSlash", "/home/user/file.txt", "/home/user")
        comparator("$dirWithoutTrailingSlash$dir", "/home/user/file.txt", "/home/user/home/user/")
        comparator("$dir$fileName", "/home/user/file.txt", "/home/user/file.txt")
        comparator("$dir$fileName", "/home/user/file", "/home/user/file")
        comparator("$fullFileName", "/home/user/file.txt", "/home/user/file.txt")
        comparator("$dir$fileNameWithoutExt", "/home/user/file", "/home/user/file")
        comparator("$dir$fileNameWithoutExt", "/home/user/file.txt", "/home/user/file")
        comparator("$dir$fileNameWithoutExt", "/home/user/file.txt.cpp", "/home/user/file.txt")
        comparator("$dir$fileNameWithoutExt$fileExt", "/home/user/file.txt.cpp", "/home/user/file.txt.cpp")
        comparator("$workspaceRoot", "/home/user/file", workspace_root)
        comparator("$workspaceRoot/$fileName", "/home/user/file.txt", f"{workspace_root}/file.txt")
        comparator("$workspaceRoot/$fileNameWithoutExt", "/home/user/file", f"{workspace_root}/file")

    class TComparator:
        def __init__(self, project_info_extractor: IProjectInfoExtractor, file_info_extractor: IFileInfoExtractor):
            self._project_info_extractor: IProjectInfoExtractor = project_info_extractor
            self._file_info_extractor: IFileInfoExtractor = file_info_extractor

        def __call__(self, pattern: str, file_path_abs: str, expected_result: str):
            builder: TInterpolatorCommandBuilder = TInterpolatorCommandBuilder(
                pattern, self._project_info_extractor, self._file_info_extractor
            )
            assert builder.build(file_path_abs) == expected_result
