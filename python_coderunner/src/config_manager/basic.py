from abc import ABC, abstractmethod
from typing import Any, Dict, List

from .config_field import TConfigField
from .interface import IConfig


class UndefinedValueError(ValueError):
    """Config value is not defined (raised by IConfigGetter)"""


class IConfigGetter(ABC):
    """Interface for getting raw config values"""

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


class TBasicConfigManager(IConfig):
    """
    Configuration manager.
    Aggregates TConfigField objects, each of which encapsulates:
    - Value retrieval
    - Validation
    - Field metadata
    - Error handling
    """

    def __init__(
        self,
        by_file_ext_field: TConfigField[Dict[str, str]],
        by_file_type_field: TConfigField[Dict[str, str]],
        by_glob_field: TConfigField[Dict[str, str]],
        dispatchers_order_field: TConfigField[List],
        coderunner_tempfile_prefix_field: TConfigField[str],
        executor_field: TConfigField[str],
        ignore_selection_field: TConfigField[bool],
        respect_shebang_field: TConfigField[bool],
        remove_coderunner_tempfiles_on_exit_field: TConfigField[bool],
        save_all_files_before_run_field: TConfigField[bool],
        save_file_before_run_field: TConfigField[bool],
    ):
        self._by_file_ext = by_file_ext_field
        self._by_file_type = by_file_type_field
        self._by_glob = by_glob_field
        self._dispatchers_order = dispatchers_order_field
        self._coderunner_tempfile_prefix = coderunner_tempfile_prefix_field
        self._executor = executor_field
        self._ignore_selection = ignore_selection_field
        self._respect_shebang = respect_shebang_field
        self._remove_coderunner_tempfiles_on_exit = remove_coderunner_tempfiles_on_exit_field
        self._save_all_files_before_run = save_all_files_before_run_field
        self._save_file_before_run = save_file_before_run_field

    def get_by_file_ext(self) -> Dict[str, str]:
        return self._by_file_ext.get()

    def get_by_file_type(self) -> Dict[str, str]:
        return self._by_file_type.get()

    def get_by_glob(self) -> Dict[str, str]:
        return self._by_glob.get()

    def get_dispatchers_order(self) -> List:
        return self._dispatchers_order.get()

    def get_coderunner_tempfile_prefix(self) -> str:
        return self._coderunner_tempfile_prefix.get()

    def get_executor(self) -> str:
        return self._executor.get()

    def get_ignore_selection(self) -> bool:
        return self._ignore_selection.get()

    def get_respect_shebang(self) -> bool:
        return self._respect_shebang.get()

    def get_remove_coderunner_tempfiles_on_exit(self) -> bool:
        return self._remove_coderunner_tempfiles_on_exit.get()

    def get_save_all_files_before_run(self) -> bool:
        return self._save_all_files_before_run.get()

    def get_save_file_before_run(self) -> bool:
        return self._save_file_before_run.get()
