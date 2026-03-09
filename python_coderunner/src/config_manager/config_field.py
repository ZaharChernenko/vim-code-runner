from typing import Any, Callable, Generic, TypeVar

from ..validators.interface import IValidator
from .exceptions import ConfigFieldNotFoundError, ConfigFieldValidationError

T = TypeVar("T")


class UndefinedValueError(Exception):
    """Config value is not defined"""


class TConfigField(Generic[T]):
    """
    Self-describing field object that encapsulates:
    - Getting value (getter)
    - Validating value (validator)
    - Field metadata (name, allowed_values)
    - Error handling
    """

    def __init__(
        self,
        name: str,
        getter: Callable[[], Any],
        validator: IValidator[T],
        allowed_values_description: str,
    ):
        self.name = name
        self.getter = getter
        self.validator = validator
        self.allowed_values_description = allowed_values_description

    def get(self) -> T:
        """Gets and validates config value"""
        try:
            raw_value = self.getter()
        except UndefinedValueError:
            raise ConfigFieldNotFoundError(self.name, self.allowed_values_description)

        try:
            return self.validator.validate(raw_value)
        except Exception as e:
            # Catch validator exception and convert it
            raise ConfigFieldValidationError(
                field_name=self.name,
                value=raw_value,
                reason=str(e),
                allowed_values=self.allowed_values_description,
            ) from e
