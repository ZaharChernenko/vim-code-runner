from abc import ABC, abstractmethod
from typing import Optional

from ..coderunner import TCodeRunner


class ICodeRunnerBuilder(ABC):
    @abstractmethod
    def build(self) -> Optional[TCodeRunner]:
        raise NotImplementedError
