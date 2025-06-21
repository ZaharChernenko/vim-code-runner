from abc import ABC, abstractmethod
from enum import StrEnum
from typing import Any, ClassVar, Dict, List


class EDispatchersTypes(StrEnum):
    BY_FILE_EXT = "by_file_ext"
    BY_FILE_TYPE = "by_file_type"
    BY_GLOB = "by_glob"


class UndefinedValueError(ValueError):
    pass


class IConfigGetter(ABC):
    @abstractmethod
    def get_by_file_ext(self) -> Any:
        raise NotImplementedError

    @abstractmethod
    def get_by_file_type(self) -> Any:
        raise NotImplementedError

    @abstractmethod
    def get_by_glob(self) -> Any:
        raise NotImplementedError

    @abstractmethod
    def get_coderunner_tempfile_prefix(self) -> Any:
        raise NotImplementedError

    @abstractmethod
    def get_dispatchers_order(self) -> Any:
        raise NotImplementedError

    @abstractmethod
    def get_executor(self) -> Any:
        raise NotImplementedError

    @abstractmethod
    def get_ignore_selection(self) -> Any:
        raise NotImplementedError

    @abstractmethod
    def get_respect_shebang(self) -> Any:
        raise NotImplementedError

    @abstractmethod
    def get_remove_coderunner_tempfiles_on_exit(self) -> Any:
        raise NotImplementedError

    @abstractmethod
    def get_save_all_files_before_run(self) -> Any:
        raise NotImplementedError

    @abstractmethod
    def get_save_file_before_run(self) -> Any:
        raise NotImplementedError


class ValidationError(ValueError):
    pass


class TBasicConfigValidator:
    def validate_bool(self, value: Any) -> bool:
        if isinstance(value, bool):
            return value
        if str(value).strip() in ("0", "1"):
            return bool(int(value))
        raise ValidationError(f"Invalid bool value: {value}.")

    def validate_str(self, value: Any) -> str:
        if isinstance(value, str):
            return value
        raise ValidationError(f"Invalid str type: {type(value)}.")

    def validate_dispatcher(self, value: Any) -> Dict[str, str]:
        if not isinstance(value, dict):
            raise ValidationError(f"Invalid dispatcher container type: {type(value)}.")
        for key, val in value.items():
            if not isinstance(key, str):
                raise ValidationError(f"Invalid type in dispatcher dict key: {type(key)}.")
            if not isinstance(val, str):
                raise ValidationError(f"Invalid type in dispatcher dict value: {type(val)}.")
        return value

    def validate_dispatchers_order(self, value: Any) -> List[EDispatchersTypes]:
        if not isinstance(value, list):
            raise ValidationError(f"Invalid dispatcher order container type: {type(value)}.")

        if invalid_items := [v for v in value if v not in EDispatchersTypes]:
            raise ValidationError(f"Invalid dispatcher types values: {', '.join(map(str, invalid_items))}.")
        return value


class TBasicConfigManager:
    by_file_ext_alias: ClassVar[str] = "by_file_ext"
    by_file_ext_allowed_values: ClassVar[str] = "Dict[str, str] value"
    by_file_type_alias: ClassVar[str] = "by_file_type"
    by_file_type_allowed_values: ClassVar[str] = "Dict[str, str] value"
    by_glob_alias: ClassVar[str] = "by_glob"
    by_glob_allowed_values: ClassVar[str] = "Dict[str, str] value"

    dispatchers_order_alias: ClassVar[str] = "runners_order"
    dispatchers_order_allowed_values: ClassVar[str] = ", ".join(
        dispatcher_type.value for dispatcher_type in EDispatchersTypes
    )

    coderunner_tempfile_prefix_alias: ClassVar[str] = "coderunner_tempfile_prefix"
    coderunner_tempfile_prefix_allowed_values: ClassVar[str] = "str value"
    executor_alias: ClassVar[str] = "executor"
    executor_allowed_values: ClassVar[str] = "str value"

    bool_allowed_values: ClassVar[str] = "0 or 1"
    ignore_selection_alias: ClassVar[str] = "ignore_selection"
    ignore_selection_allowed_values: ClassVar[str] = bool_allowed_values
    respect_shebang_alias: ClassVar[str] = "respect_shebang"
    respect_shebang_allowed_values: ClassVar[str] = bool_allowed_values
    remove_coderunner_tempfiles_on_exit_alias: ClassVar[str] = "coderunner_remove_coderunner_tempfiles_on_exit"
    remove_coderunner_tempfiles_on_exit_allowed_values: ClassVar[str] = bool_allowed_values
    save_all_files_before_run_alias: ClassVar[str] = "save_all_files_before_run"
    save_all_files_before_run_allowed_values: ClassVar[str] = bool_allowed_values
    save_file_before_run_alias: ClassVar[str] = "save_file_before_run"
    save_file_before_run_allowed_values: ClassVar[str] = bool_allowed_values

    def __init__(self, config_getter: IConfigGetter, config_validator: TBasicConfigValidator):
        self._config_getter: IConfigGetter = config_getter
        self._config_validator: TBasicConfigValidator = config_validator

    def get_by_file_ext(self) -> Dict[str, str]:
        try:
            raw_value: Any = self._config_getter.get_by_file_ext()
            validated_value: Dict[str, str] = self._config_validator.validate_dispatcher(raw_value)
            return validated_value
        except UndefinedValueError as e:
            raise ValueError(self._format_undefined_value_error_message(e, self.by_file_ext_allowed_values))
        except ValidationError as e:
            raise ValueError(
                self._format_validation_error_message(e, self.by_file_ext_alias, self.by_file_ext_allowed_values)
            )

    def get_by_file_type(self) -> Dict[str, str]:
        try:
            raw_value: Any = self._config_getter.get_by_file_type()
            validated_value: Dict[str, str] = self._config_validator.validate_dispatcher(raw_value)
            return validated_value
        except UndefinedValueError as e:
            raise ValueError(self._format_undefined_value_error_message(e, self.by_file_type_allowed_values))
        except ValidationError as e:
            raise ValueError(
                self._format_validation_error_message(e, self.by_file_type_alias, self.by_file_type_allowed_values)
            )

    def get_by_glob(self) -> Dict[str, str]:
        try:
            raw_value: Any = self._config_getter.get_by_glob()
            validated_value: Dict[str, str] = self._config_validator.validate_dispatcher(raw_value)
            return validated_value
        except UndefinedValueError as e:
            raise ValueError(self._format_undefined_value_error_message(e, self.by_glob_allowed_values))
        except ValidationError as e:
            raise ValueError(self._format_validation_error_message(e, self.by_glob_alias, self.by_glob_allowed_values))

    def get_dispatchers_order(self) -> List[EDispatchersTypes]:
        try:
            raw_value: Any = self._config_getter.get_dispatchers_order()
            validated_value: List[EDispatchersTypes] = self._config_validator.validate_dispatchers_order(raw_value)
            return validated_value
        except UndefinedValueError as e:
            raise ValueError(self._format_undefined_value_error_message(e, self.dispatchers_order_allowed_values))
        except ValidationError as e:
            raise ValueError(
                self._format_validation_error_message(
                    e, self.dispatchers_order_alias, self.dispatchers_order_allowed_values
                )
            )

    def get_coderunner_tempfile_prefix(self) -> str:
        try:
            raw_value: Any = self._config_getter.get_coderunner_tempfile_prefix()
            validated_value: str = self._config_validator.validate_str(raw_value)
            return validated_value
        except UndefinedValueError as e:
            raise ValueError(
                self._format_undefined_value_error_message(e, self.coderunner_tempfile_prefix_allowed_values)
            )
        except ValidationError as e:
            raise ValueError(
                self._format_validation_error_message(
                    e, self.coderunner_tempfile_prefix_alias, self.coderunner_tempfile_prefix_allowed_values
                )
            )

    def get_executor(self) -> str:
        try:
            raw_value: Any = self._config_getter.get_executor()
            validated_value: str = self._config_validator.validate_str(raw_value)
            return validated_value
        except UndefinedValueError as e:
            raise ValueError(self._format_undefined_value_error_message(e, self.executor_allowed_values))
        except ValidationError as e:
            raise ValueError(
                self._format_validation_error_message(e, self.executor_alias, self.executor_allowed_values)
            )

    def get_ignore_selection(self) -> bool:
        try:
            raw_value: Any = self._config_getter.get_ignore_selection()
            validated_value: bool = self._config_validator.validate_bool(raw_value)
            return validated_value
        except UndefinedValueError as e:
            raise ValueError(self._format_undefined_value_error_message(e, self.ignore_selection_allowed_values))
        except ValidationError as e:
            raise ValueError(
                self._format_validation_error_message(
                    e, self.ignore_selection_alias, self.ignore_selection_allowed_values
                )
            )

    def get_respect_shebang(self) -> bool:
        try:
            raw_value: Any = self._config_getter.get_respect_shebang()
            validated_value: bool = self._config_validator.validate_bool(raw_value)
            return validated_value
        except UndefinedValueError as e:
            raise ValueError(self._format_undefined_value_error_message(e, self.respect_shebang_allowed_values))
        except ValidationError as e:
            raise ValueError(
                self._format_validation_error_message(
                    e, self.respect_shebang_alias, self.respect_shebang_allowed_values
                )
            )

    def get_remove_coderunner_tempfiles_on_exit(self) -> bool:
        try:
            raw_value: Any = self._config_getter.get_remove_coderunner_tempfiles_on_exit()
            validated_value: bool = self._config_validator.validate_bool(raw_value)
            return validated_value
        except UndefinedValueError as e:
            raise ValueError(
                self._format_undefined_value_error_message(e, self.remove_coderunner_tempfiles_on_exit_allowed_values)
            )
        except ValidationError as e:
            raise ValueError(
                self._format_validation_error_message(
                    e,
                    self.remove_coderunner_tempfiles_on_exit_alias,
                    self.remove_coderunner_tempfiles_on_exit_allowed_values,
                )
            )

    def get_save_all_files_before_run(self) -> bool:
        try:
            raw_value: Any = self._config_getter.get_save_all_files_before_run()
            validated_value: bool = self._config_validator.validate_bool(raw_value)
            return validated_value
        except UndefinedValueError as e:
            raise ValueError(
                self._format_undefined_value_error_message(e, self.save_all_files_before_run_allowed_values)
            )
        except ValidationError as e:
            raise ValueError(
                self._format_validation_error_message(
                    e, self.save_all_files_before_run_alias, self.save_all_files_before_run_allowed_values
                )
            )

    def get_save_file_before_run(self) -> bool:
        try:
            raw_value: Any = self._config_getter.get_save_file_before_run()
            validated_value: bool = self._config_validator.validate_bool(raw_value)
            return validated_value
        except UndefinedValueError as e:
            raise ValueError(self._format_undefined_value_error_message(e, self.save_file_before_run_allowed_values))
        except ValidationError as e:
            raise ValueError(
                self._format_validation_error_message(
                    e, self.save_file_before_run_alias, self.save_file_before_run_allowed_values
                )
            )

    def _format_undefined_value_error_message(self, e: UndefinedValueError, allowed_values: str) -> str:
        return f"{e} Allowed values: {allowed_values}."

    def _format_validation_error_message(self, e: ValidationError, var_alias: str, allowed_values: str) -> str:
        return f"Invalid value of the {var_alias} variable. {e} Allowed values: {allowed_values}."
