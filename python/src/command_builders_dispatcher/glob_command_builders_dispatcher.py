import re
from typing import Final, Optional, Tuple

from src.command_builder import ICommandBuilder
from src.command_builders_dispatcher.interface import ICommandBuildersDispatcher


class TGlobCommandBuildersDispatcher(ICommandBuildersDispatcher):
    def __init__(self, glob_to_builder: Tuple[Tuple[re.Pattern, ICommandBuilder], ...]):
        self._glob_to_builder: Final[Tuple[Tuple[re.Pattern, ICommandBuilder], ...]] = glob_to_builder

    def dispatch(self, file_path_abs: str) -> Optional[ICommandBuilder]:
        for pattern, builder in self._glob_to_builder:
            if pattern.match(file_path_abs):
                return builder
        return None
