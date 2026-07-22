from typing import ClassVar

from ..file_info_extractor import IFileInfoExtractor
from ..project_info_extractor import IProjectInfoExtractor
from .interface import ICommandBuilder


class TInterpolatorCommandBuilder(ICommandBuilder):
    _WORKSPACE_ROOT_VAR: ClassVar[str] = "$workspaceRoot"
    _FULL_FILE_NAME_VAR: ClassVar[str] = "$fullFileName"
    _FILE_NAME_WITHOUT_EXT_VAR: ClassVar[str] = "$fileNameWithoutExt"
    _FILE_NAME_VAR: ClassVar[str] = "$fileName"
    _FILE_EXT_VAR: ClassVar[str] = "$fileExt"
    _DRIVE_LETTER_VAR: ClassVar[str] = "$driveLetter"
    _DIR_WITHOUT_TRAILING_SLASH_VAR: ClassVar[str] = "$dirWithoutTrailingSlash"
    _DIR_VAR: ClassVar[str] = "$dir"

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
        interpolated_str: str = self._template_string.replace(
            self._WORKSPACE_ROOT_VAR, self._project_info_extractor.get_workspace_root()
        )
        interpolated_str = interpolated_str.replace(self._FULL_FILE_NAME_VAR, file_path_abs)
        interpolated_str = interpolated_str.replace(
            self._FILE_NAME_WITHOUT_EXT_VAR, self._file_info_extractor.get_file_name_without_ext(file_path_abs)
        )
        interpolated_str = interpolated_str.replace(
            self._FILE_NAME_VAR, self._file_info_extractor.get_file_name(file_path_abs)
        )
        interpolated_str = interpolated_str.replace(
            self._FILE_EXT_VAR, self._file_info_extractor.get_file_ext(file_path_abs)
        )
        interpolated_str = interpolated_str.replace(
            self._DRIVE_LETTER_VAR, self._file_info_extractor.get_drive_letter(file_path_abs)
        )
        interpolated_str = interpolated_str.replace(
            self._DIR_WITHOUT_TRAILING_SLASH_VAR,
            self._file_info_extractor.get_dir_without_trailing_slash(file_path_abs),
        )
        interpolated_str = interpolated_str.replace(self._DIR_VAR, self._file_info_extractor.get_dir(file_path_abs))

        return interpolated_str
