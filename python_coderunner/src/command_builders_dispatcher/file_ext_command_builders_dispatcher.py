from typing import Dict, Final, Optional

from ..command_builder import ICommandBuilder
from ..file_info_extractor import IFileInfoExtractor
from .interface import ICommandBuildersDispatcher


class TFileExtCommandBuildersDispatcher(ICommandBuildersDispatcher):
    def __init__(self, file_ext_to_builder: Dict[str, ICommandBuilder], file_info_extractor: IFileInfoExtractor):
        self._file_ext_to_builder: Final[Dict[str, ICommandBuilder]] = file_ext_to_builder
        self._file_info_extractor: IFileInfoExtractor = file_info_extractor

    def dispatch(self, file_path_abs: str) -> Optional[ICommandBuilder]:
        file_ext: str = self._file_info_extractor.get_file_ext(file_path_abs)
        return self._file_ext_to_builder.get(file_ext)
