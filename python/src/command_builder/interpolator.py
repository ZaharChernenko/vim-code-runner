import re
from typing import ClassVar

from src.command_builder.interface import ICommandBuilder
from src.file_info_extractor import IFileInfoExtractor


class TInterpolatorCommandBuilder(ICommandBuilder):
    WORKSPACE_ROOT_PATTERN: ClassVar[re.Pattern] = re.compile(r"\$workspaceRoot")
    FULL_FILE_NAME_PATTERN: ClassVar[re.Pattern] = re.compile(r"\$fullFileName")
    FILE_NAME_WITHOUT_EXT_PATTERN: ClassVar[re.Pattern] = re.compile(r"\$fileNameWithoutExt")
    FILE_NAME_PATTERN: ClassVar[re.Pattern] = re.compile(r"\$fileName")
    FILE_EXT: ClassVar[re.Pattern] = re.compile(r"\$fileExt")
    DRIVE_LETTER_PATTERN: ClassVar[re.Pattern] = re.compile(r"\$driveLetter")
    DIR_WITHOUT_TRAILING_SLASH_PATTERN: ClassVar[re.Pattern] = re.compile(r"\$dirWithoutTrailingSlash")
    DIR_PATTERN: ClassVar[re.Pattern] = re.compile(r"\$dir")

    def __init__(self, template_string: str, file_info_extractor: IFileInfoExtractor):
        self._template_string: str = template_string
        self._file_info_extractor: IFileInfoExtractor = file_info_extractor

    def build(self, file_path_abs: str) -> str:
        return self._interpolate(file_path_abs)

    def _interpolate(self, file_path_abs: str) -> str:
        """
        The reverse alphabetical order is important so that substitutions are performed greedily,
        i.e. $dirWithoutTrailingSlash must be before $dir.
        """
        interpolated_str: str = self.WORKSPACE_ROOT_PATTERN.sub(
            self._file_info_extractor.get_workspace_root(file_path_abs), self._template_string
        )
        interpolated_str = self.FULL_FILE_NAME_PATTERN.sub(
            self._file_info_extractor.get_full_file_name(file_path_abs), interpolated_str
        )
        interpolated_str = self.FILE_NAME_WITHOUT_EXT_PATTERN.sub(
            self._file_info_extractor.get_file_name_without_ext(file_path_abs), interpolated_str
        )
        interpolated_str = self.FILE_NAME_PATTERN.sub(
            self._file_info_extractor.get_file_name(file_path_abs), interpolated_str
        )
        interpolated_str = self.FILE_EXT.sub(self._file_info_extractor.get_file_ext(file_path_abs), interpolated_str)
        interpolated_str = self.DRIVE_LETTER_PATTERN.sub(
            self._file_info_extractor.get_drive_letter(file_path_abs), interpolated_str
        )
        interpolated_str = self.DIR_WITHOUT_TRAILING_SLASH_PATTERN.sub(
            self._file_info_extractor.get_dir_without_trailing_slash(file_path_abs), interpolated_str
        )
        interpolated_str = self.DIR_PATTERN.sub(self._file_info_extractor.get_dir(file_path_abs), interpolated_str)

        return interpolated_str
