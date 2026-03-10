from abc import ABC, abstractmethod


class ICommandsExecutor(ABC):
    """
    Class for executing a string command only.
    """

    @abstractmethod
    def execute(self, command: str) -> None:
        raise NotImplementedError
