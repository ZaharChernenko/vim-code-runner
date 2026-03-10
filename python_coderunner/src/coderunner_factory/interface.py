from abc import ABC, abstractmethod

from ..coderunner import TCodeRunner


class ICodeRunnerFactory(ABC):
    @abstractmethod
    def create(self) -> TCodeRunner | None:
        raise NotImplementedError
