from abc import ABC, abstractmethod
from typing import Optional

from ..command_builder import ICommandBuilder


class ICommandBuildersDispatcher(ABC):
    @abstractmethod
    def dispatch(self, file_path_abs: str) -> Optional[ICommandBuilder]:
        """
        Dispatch is optional for fallback strategy.
        """
        raise NotImplementedError
