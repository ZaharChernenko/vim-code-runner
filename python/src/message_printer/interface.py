import abc


class IMessagePrinter(abc.ABC):
    def error(self, text: str) -> None:
        raise NotImplementedError

    def info(self, text: str) -> None:
        raise NotImplementedError
