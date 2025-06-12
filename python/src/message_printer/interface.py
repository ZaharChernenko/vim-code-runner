from abc import ABC, abstractmethod


class IMessagePrinter(ABC):
    @abstractmethod
    def error(self, text: str) -> None:
        raise NotImplementedError

    @abstractmethod
    def info(self, text: str) -> None:
        raise NotImplementedError
