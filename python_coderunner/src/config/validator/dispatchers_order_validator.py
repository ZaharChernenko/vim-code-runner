from typing import Any

from ..interface import EDispatchersTypes
from .exceptions import ValidationError
from .interface import IValidator


class TDispatchersOrderValidator(IValidator[list[EDispatchersTypes]]):
    def __init__(self) -> None:
        self.allowed_dispatcher_types: set[EDispatchersTypes] = set(EDispatchersTypes)

    def __call__(self, value: Any) -> list[EDispatchersTypes]:
        if not isinstance(value, list):
            raise ValidationError(f"Invalid dispatcher order container type: {type(value)}.")

        if invalid_items := [v for v in value if v not in self.allowed_dispatcher_types]:
            raise ValidationError(f"Invalid dispatcher types values: {', '.join(map(str, invalid_items))}.")

        return value
