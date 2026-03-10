from typing import Any, Generic, TypeVar

from .exceptions import ConfigFieldUndefinedValueError, ConfigFieldValidationError
from .getter import IConfigValueGetter, UndefinedValueError
from .validator import IValidator, ValidationError

ValueType = TypeVar("ValueType")


class TConfigField(Generic[ValueType]):
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
        getter: IConfigValueGetter,
        validator: IValidator[ValueType],
        allowed_values_description: str,
    ):
        self._name: str = name
        self._getter: IConfigValueGetter = getter
        self._validator: IValidator[ValueType] = validator
        self._allowed_values_description: str = allowed_values_description

    def get(self) -> ValueType:
        try:
            raw_value: Any = self._getter()
        except UndefinedValueError as e:
            raise ConfigFieldUndefinedValueError.from_undefined_value_error(e, self._allowed_values_description)

        try:
            return self._validator(raw_value)
        except ValidationError as e:
            raise ConfigFieldValidationError.from_validation_error(e, self._name, self._allowed_values_description)
