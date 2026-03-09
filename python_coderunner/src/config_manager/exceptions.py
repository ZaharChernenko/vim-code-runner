from typing import Any


class ConfigFieldNotFoundError(Exception):
    """Поле конфига не найдено"""

    def __init__(self, field_name: str, allowed_values: str):
        self.field_name = field_name
        self.allowed_values = allowed_values
        super().__init__(f"Config parameter '{field_name}' not defined. Allowed values: {allowed_values}.")


class ConfigFieldValidationError(Exception):
    """Значение поля конфига некорректно"""

    def __init__(self, field_name: str, value: Any, reason: str, allowed_values: str):
        self.field_name = field_name
        self.value = value
        self.reason = reason
        self.allowed_values = allowed_values
        super().__init__(f"Invalid value of {field_name}: {reason}. Got: {value}. Allowed values: {allowed_values}.")
