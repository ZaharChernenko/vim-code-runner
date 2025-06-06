import abc
from typing import Optional

from src.command_builder import ICommandBuilder


class ICommandBuildersDispatcher(abc.ABC):
    @abc.abstractmethod
    def dispatch(self, file_path_abs: str) -> Optional[ICommandBuilder]:
        """
        Dispatch is optional for fallback strategy.
        """
        raise NotImplementedError
