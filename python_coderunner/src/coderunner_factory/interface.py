from abc import ABC, abstractmethod
from typing import Optional

from ..coderunner import TCodeRunner


class ICodeRunnerFactory(ABC):
    @abstractmethod
    def create(self) -> Optional[TCodeRunner]:
        raise NotImplementedError
