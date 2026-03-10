import re
from typing import Final

from ..command_builder import ICommandBuilder
from .interface import ICommandBuildersDispatcher


class TGlobCommandBuildersDispatcher(ICommandBuildersDispatcher):
    def __init__(self, glob_to_builder: tuple[tuple[re.Pattern[str], ICommandBuilder], ...]):
        self._glob_to_builder: Final[tuple[tuple[re.Pattern[str], ICommandBuilder], ...]] = glob_to_builder

    def dispatch(self, file_path_abs: str) -> ICommandBuilder | None:
        for pattern, builder in self._glob_to_builder:
            if pattern.match(file_path_abs):
                return builder
        return None
