from typing import Dict, Final, Optional

from ..command_builder import ICommandBuilder
from ..file_info_extractor import IFileInfoExtractor
from .interface import ICommandBuildersDispatcher


class TFileTypeCommandBuildersDispatcher(ICommandBuildersDispatcher):
    def __init__(self, file_type_to_builder: Dict[str, ICommandBuilder], file_info_extractor: IFileInfoExtractor):
        self._file_type_to_builder: Final[Dict[str, ICommandBuilder]] = file_type_to_builder
        self._file_info_extractor: IFileInfoExtractor = file_info_extractor

    def dispatch(self, file_path_abs: str) -> Optional[ICommandBuilder]:
        file_type: Optional[str] = self._file_info_extractor.get_file_type(file_path_abs)
        if file_type is None:
            return None
        return self._file_type_to_builder.get(file_type)
