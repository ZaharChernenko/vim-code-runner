from abc import ABC, abstractmethod

from ..command_builder import ICommandBuilder


class ICommandBuildersDispatcher(ABC):
    @abstractmethod
    def dispatch(self, file_path_abs: str) -> ICommandBuilder | None:
        """
        Dispatch is optional for fallback strategy.
        """
        raise NotImplementedError
