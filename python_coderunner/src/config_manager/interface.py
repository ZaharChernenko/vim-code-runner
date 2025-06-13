from abc import ABC, abstractmethod
from enum import StrEnum
from typing import Any, Dict, List


class EDispatchersTypes(StrEnum):
    BY_FILE_TYPE = "by_file_type"
    BY_FILE_EXT = "by_file_ext"
    BY_GLOB = "by_glob"


class IConfigManager(ABC):
    def get_glob_to_command(self) -> Dict[str, str]:
        return self._validate_dispatcher(self._get_glob_to_command_impl())

    def get_file_ext_to_command(self) -> Dict[str, str]:
        return self._validate_dispatcher(self._get_file_ext_to_command_impl())

    def get_file_type_to_command(self) -> Dict[str, str]:
        return self._validate_dispatcher(self._get_file_type_to_command_impl())

    def get_dispatchers_order(self) -> List[EDispatchersTypes]:
        return self._validate_dispatchers_order(self._get_dispatchers_order_impl())

    def get_executor(self) -> str:
        return self._get_executor_impl()

    def get_ignore_selection(self) -> bool:
        return self._validate_bool(self._get_ignore_selection_impl())

    def get_respect_shebang(self) -> bool:
        return self._validate_bool(self._get_respect_shebang_impl())

    def get_save_all_files(self) -> bool:
        return self._validate_bool(self._get_save_all_files_impl())

    def get_save_file(self) -> bool:
        return self._validate_bool(self._get_save_file_impl())

    @abstractmethod
    def _get_glob_to_command_impl(self) -> Any:
        raise NotImplementedError

    @abstractmethod
    def _get_file_ext_to_command_impl(self) -> Any:
        raise NotImplementedError

    @abstractmethod
    def _get_file_type_to_command_impl(self) -> Any:
        raise NotImplementedError

    @abstractmethod
    def _get_dispatchers_order_impl(self) -> Any:
        raise NotImplementedError

    @abstractmethod
    def _get_executor_impl(self) -> Any:
        raise NotImplementedError

    @abstractmethod
    def _get_ignore_selection_impl(self) -> Any:
        raise NotImplementedError

    @abstractmethod
    def _get_respect_shebang_impl(self) -> Any:
        raise NotImplementedError

    @abstractmethod
    def _get_save_all_files_impl(self) -> Any:
        raise NotImplementedError

    @abstractmethod
    def _get_save_file_impl(self) -> Any:
        raise NotImplementedError

    def _validate_bool(self, value: Any) -> bool:
        if isinstance(value, bool):
            return value
        if str(value).strip() in ("0", "1"):
            return bool(int(value))
        raise ValueError(f"Expected 0 or 1, got: {value}")

    def _validate_dispatcher(self, value: Any) -> Dict[str, str]:
        if not isinstance(value, dict):
            raise ValueError(f"Expected dict, got: {type(value)}")
        for key, val in value.items():
            if not (isinstance(key, str) and isinstance(val, str)):
                raise ValueError(f"Expected str, got: {type(value)}")
        return value

    def _validate_dispatchers_order(self, value: Any) -> List[EDispatchersTypes]:
        if not isinstance(value, list):
            raise ValueError(f"Expected list, got: {type(value)}")

        if invalid_items := [v for v in value if v not in EDispatchersTypes]:
            raise ValueError(
                f"Invalid dispatcher types: {invalid_items}. Allowed: {[dispatcher_type.value for dispatcher_type in EDispatchersTypes]}"
            )
        return value
