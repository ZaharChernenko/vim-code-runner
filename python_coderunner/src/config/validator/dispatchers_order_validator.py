from typing import Any, ClassVar

from ..interface import EDispatchersTypes
from .exceptions import ValidationError
from .interface import IValidator


class TDispatchersOrderValidator(IValidator[list[EDispatchersTypes]]):
    _ALLOWED_DISPATCHER_TYPES: ClassVar[set[EDispatchersTypes]] = set(EDispatchersTypes)

    def __call__(self, value: Any) -> list[EDispatchersTypes]:
        if not isinstance(value, list):
            raise ValidationError(f"Invalid dispatcher order container type: {type(value)}.")

        if invalid_items := [v for v in value if v not in self._ALLOWED_DISPATCHER_TYPES]:
            raise ValidationError(f"Invalid dispatcher types values: {', '.join(map(str, invalid_items))}.")

        return value
