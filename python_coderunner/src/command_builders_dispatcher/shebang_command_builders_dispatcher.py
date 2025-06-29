from typing import Optional

from src.command_builder import ICommandBuilder, TConcatenatorCommandBuilder
from src.command_builders_dispatcher.interface import ICommandBuildersDispatcher
from src.file_info_extractor import IFileInfoExtractor


class TShebangCommandBuildersDispatcher(ICommandBuildersDispatcher):
    def __init__(self, file_info_extractor: IFileInfoExtractor):
        self._file_info_extractor: IFileInfoExtractor = file_info_extractor

    def dispatch(self, file_path_abs: str) -> Optional[ICommandBuilder]:
        if (shebang := self._file_info_extractor.get_shebang(file_path_abs)) is not None:
            return TConcatenatorCommandBuilder(shebang)
        return None
