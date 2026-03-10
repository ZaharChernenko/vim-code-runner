from abc import ABC, abstractmethod
from typing import Any


class IConfigValueGetter(ABC):
    @abstractmethod
    def __call__(self) -> Any:
        """
        Gets config value from external source.

        Raises:
            UndefinedValueError: If the config value is not defined.
        """
        raise NotImplementedError
