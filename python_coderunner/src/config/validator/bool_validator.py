from typing import Any

from .exceptions import ValidationError
from .interface import IValidator


class TBoolValidator(IValidator[bool]):
    def __call__(self, value: Any) -> bool:
        if isinstance(value, bool):
            return value
        if str(value).strip() in ("0", "1"):
            return bool(int(value))
        raise ValidationError(f"Invalid bool value: {value}.")
