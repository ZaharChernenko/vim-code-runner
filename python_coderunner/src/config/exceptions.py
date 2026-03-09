from typing import Any, Self

from ..validators import ValidationError
from .getter import UndefinedValueError


class ConfigFieldNotFoundError(UndefinedValueError):
    @classmethod
    def from_undefined_value_error(cls, e: UndefinedValueError, allowed_values: str) -> Self:
        return cls(f"{e} Allowed values: {allowed_values}.")


class ConfigFieldValidationError(ValidationError):
    @classmethod
    def from_validation_error(cls, e: ValidationError, field_name: str, allowed_values: str) -> Self:
        return cls(f"Invalid value of {field_name}. {e} Allowed values: {allowed_values}.")
