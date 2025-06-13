from abc import ABC, abstractmethod


class ICommandsExecutor(ABC):
    """
    Сlass for executing a string command only.
    """

    @abstractmethod
    def execute(self, command: str) -> None:
        raise NotImplementedError
