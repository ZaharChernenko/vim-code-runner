from typing import Any

from .exceptions import ValidationError
from .interface import IValidator


class TStrValidator(IValidator[str]):
    def __call__(self, value: Any) -> str:
        if isinstance(value, str):
            return value
        raise ValidationError(f"Invalid str type: {type(value)}.")
