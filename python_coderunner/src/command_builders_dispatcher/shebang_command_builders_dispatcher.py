from typing import Optional

from ..command_builder import ICommandBuilder, TConcatenatorCommandBuilder
from ..file_info_extractor import IFileInfoExtractor
from .interface import ICommandBuildersDispatcher


class TShebangCommandBuildersDispatcher(ICommandBuildersDispatcher):
    def __init__(self, file_info_extractor: IFileInfoExtractor):
        self._file_info_extractor: IFileInfoExtractor = file_info_extractor

    def dispatch(self, file_path_abs: str) -> Optional[ICommandBuilder]:
        if (shebang := self._file_info_extractor.get_shebang(file_path_abs)) is not None:
            return TConcatenatorCommandBuilder(shebang)
        return None
