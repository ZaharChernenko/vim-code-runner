from abc import ABC, abstractmethod
from typing import Any, Generic, TypeVar

ValueType = TypeVar("ValueType")


class IValidator(ABC, Generic[ValueType]):
    """Base interface for all validators"""

    @abstractmethod
    def __call__(self, value: Any) -> ValueType:
        """
        Validates value and returns typed result.
        Raises ValidationError on validation failure.
        """
        raise NotImplementedError
