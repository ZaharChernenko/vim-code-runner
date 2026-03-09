from typing import Final

from ..command_builder import ICommandBuilder
from ..file_info_extractor import IFileInfoExtractor
from .interface import ICommandBuildersDispatcher


class TFileTypeCommandBuildersDispatcher(ICommandBuildersDispatcher):
    def __init__(self, file_type_to_builder: dict[str, ICommandBuilder], file_info_extractor: IFileInfoExtractor):
        self._file_type_to_builder: Final[dict[str, ICommandBuilder]] = file_type_to_builder
        self._file_info_extractor: IFileInfoExtractor = file_info_extractor

    def dispatch(self, file_path_abs: str) -> ICommandBuilder | None:
        file_type: str | None = self._file_info_extractor.get_file_type(file_path_abs)
        if file_type is None:
            return None
        return self._file_type_to_builder.get(file_type)
