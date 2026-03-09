from typing import Dict, List, TypeVar

from .config_field import TConfigField
from .exceptions import ConfigFieldNotFoundError, ConfigFieldValidationError
from .interface import EDispatchersTypes, IConfig

ValueType = TypeVar("ValueType")


class TBasicConfig(IConfig):
    def __init__(
        self,
        by_file_ext_field: TConfigField[Dict[str, str]],
        by_file_type_field: TConfigField[Dict[str, str]],
        by_glob_field: TConfigField[Dict[str, str]],
        dispatchers_order_field: TConfigField[List[EDispatchersTypes]],
        coderunner_tempfile_prefix_field: TConfigField[str],
        executor_field: TConfigField[str],
        ignore_selection_field: TConfigField[bool],
        respect_shebang_field: TConfigField[bool],
        remove_coderunner_tempfiles_on_exit_field: TConfigField[bool],
        save_all_files_before_run_field: TConfigField[bool],
        save_file_before_run_field: TConfigField[bool],
    ):
        self._by_file_ext_field: TConfigField[Dict[str, str]] = by_file_ext_field
        self._by_file_type_field: TConfigField[Dict[str, str]] = by_file_type_field
        self._by_glob_field: TConfigField[Dict[str, str]] = by_glob_field
        self._dispatchers_order_field: TConfigField[List[EDispatchersTypes]] = dispatchers_order_field
        self._coderunner_tempfile_prefix_field: TConfigField[str] = coderunner_tempfile_prefix_field
        self._executor_field: TConfigField[str] = executor_field
        self._ignore_selection_field: TConfigField[bool] = ignore_selection_field
        self._respect_shebang_field: TConfigField[bool] = respect_shebang_field
        self._remove_coderunner_tempfiles_on_exit_field: TConfigField[bool] = remove_coderunner_tempfiles_on_exit_field
        self._save_all_files_before_run_field: TConfigField[bool] = save_all_files_before_run_field
        self._save_file_before_run_field: TConfigField[bool] = save_file_before_run_field

    def _get_field_value(self, field: TConfigField[ValueType]) -> ValueType:
        """
        Get field value, converting ConfigField exceptions to ValueError.
        Preserves exception chain with 'raise from'.
        """
        try:
            return field.get()
        except (ConfigFieldNotFoundError, ConfigFieldValidationError) as e:
            raise ValueError(str(e)) from e

    def get_by_file_ext(self) -> Dict[str, str]:
        return self._get_field_value(self._by_file_ext_field)

    def get_by_file_type(self) -> Dict[str, str]:
        return self._get_field_value(self._by_file_type_field)

    def get_by_glob(self) -> Dict[str, str]:
        return self._get_field_value(self._by_glob_field)

    def get_dispatchers_order(self) -> List[EDispatchersTypes]:
        return self._get_field_value(self._dispatchers_order_field)

    def get_coderunner_tempfile_prefix(self) -> str:
        return self._get_field_value(self._coderunner_tempfile_prefix_field)

    def get_executor(self) -> str:
        return self._get_field_value(self._executor_field)

    def get_ignore_selection(self) -> bool:
        return self._get_field_value(self._ignore_selection_field)

    def get_respect_shebang(self) -> bool:
        return self._get_field_value(self._respect_shebang_field)

    def get_remove_coderunner_tempfiles_on_exit(self) -> bool:
        return self._get_field_value(self._remove_coderunner_tempfiles_on_exit_field)

    def get_save_all_files_before_run(self) -> bool:
        return self._get_field_value(self._save_all_files_before_run_field)

    def get_save_file_before_run(self) -> bool:
        return self._get_field_value(self._save_file_before_run_field)
