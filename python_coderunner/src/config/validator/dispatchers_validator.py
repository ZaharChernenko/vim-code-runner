from typing import Any, Dict

from .exceptions import ValidationError
from .interface import IValidator


class TDispatchersValidator(IValidator[Dict[str, str]]):
    def __call__(self, value: Any) -> Dict[str, str]:
        if not isinstance(value, dict):
            raise ValidationError(f"Invalid dispatcher container type: {type(value)}.")
        for key, val in value.items():
            if not isinstance(key, str):
                raise ValidationError(f"Invalid type in dispatcher dict key: {type(key)}.")
            if not isinstance(val, str):
                raise ValidationError(f"Invalid type in dispatcher dict value: {type(val)}.")

        return value
