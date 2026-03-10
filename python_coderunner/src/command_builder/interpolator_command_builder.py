import re
from typing import ClassVar

from ..file_info_extractor import IFileInfoExtractor
from ..project_info_extractor import IProjectInfoExtractor
from .interface import ICommandBuilder


class TInterpolatorCommandBuilder(ICommandBuilder):
    _WORKSPACE_ROOT_PATTERN: ClassVar[re.Pattern[str]] = re.compile(r"\$workspaceRoot")
    _FULL_FILE_NAME_PATTERN: ClassVar[re.Pattern[str]] = re.compile(r"\$fullFileName")
    _FILE_NAME_WITHOUT_EXT_PATTERN: ClassVar[re.Pattern[str]] = re.compile(r"\$fileNameWithoutExt")
    _FILE_NAME_PATTERN: ClassVar[re.Pattern[str]] = re.compile(r"\$fileName")
    _FILE_EXT: ClassVar[re.Pattern[str]] = re.compile(r"\$fileExt")
    _DRIVE_LETTER_PATTERN: ClassVar[re.Pattern[str]] = re.compile(r"\$driveLetter")
    _DIR_WITHOUT_TRAILING_SLASH_PATTERN: ClassVar[re.Pattern[str]] = re.compile(r"\$dirWithoutTrailingSlash")
    _DIR_PATTERN: ClassVar[re.Pattern[str]] = re.compile(r"\$dir")

    def __init__(
        self,
        template_string: str,
        project_info_extractor: IProjectInfoExtractor,
        file_info_extractor: IFileInfoExtractor,
    ):
        self._template_string: str = template_string
        self._project_info_extractor: IProjectInfoExtractor = project_info_extractor
        self._file_info_extractor: IFileInfoExtractor = file_info_extractor

    def build(self, file_path_abs: str) -> str:
        return self._interpolate(file_path_abs)

    def _interpolate(self, file_path_abs: str) -> str:
        """
        The reverse alphabetical order is important so that substitutions are performed greedily,
        i.e. $dirWithoutTrailingSlash must be before $dir.
        """
        interpolated_str: str = self._WORKSPACE_ROOT_PATTERN.sub(
            self._project_info_extractor.get_workspace_root(), self._template_string
        )
        interpolated_str = self._FULL_FILE_NAME_PATTERN.sub(file_path_abs, interpolated_str)
        interpolated_str = self._FILE_NAME_WITHOUT_EXT_PATTERN.sub(
            self._file_info_extractor.get_file_name_without_ext(file_path_abs), interpolated_str
        )
        interpolated_str = self._FILE_NAME_PATTERN.sub(
            self._file_info_extractor.get_file_name(file_path_abs), interpolated_str
        )
        interpolated_str = self._FILE_EXT.sub(self._file_info_extractor.get_file_ext(file_path_abs), interpolated_str)
        interpolated_str = self._DRIVE_LETTER_PATTERN.sub(
            self._file_info_extractor.get_drive_letter(file_path_abs), interpolated_str
        )
        interpolated_str = self._DIR_WITHOUT_TRAILING_SLASH_PATTERN.sub(
            self._file_info_extractor.get_dir_without_trailing_slash(file_path_abs), interpolated_str
        )
        interpolated_str = self._DIR_PATTERN.sub(self._file_info_extractor.get_dir(file_path_abs), interpolated_str)

        return interpolated_str
