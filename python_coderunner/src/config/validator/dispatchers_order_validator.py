from typing import Any, List, Set

from ..interface import EDispatchersTypes
from .exceptions import ValidationError
from .interface import IValidator


class TDispatchersOrderValidator(IValidator[List[EDispatchersTypes]]):
    def __init__(self) -> None:
        self.allowed_dispatcher_types: Set[EDispatchersTypes] = set(EDispatchersTypes)

    def __call__(self, value: Any) -> List[EDispatchersTypes]:
        if not isinstance(value, list):
            raise ValidationError(f"Invalid dispatcher order container type: {type(value)}.")

        if invalid_items := [v for v in value if v not in self.allowed_dispatcher_types]:
            raise ValidationError(f"Invalid dispatcher types values: {', '.join(map(str, invalid_items))}.")
        return value
