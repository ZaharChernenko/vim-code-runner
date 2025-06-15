from typing import Any, ClassVar

import vim

from src.config_manager.basic import (
    IConfigGetter,
    TBasicConfigManager,
    UndefinedValueError,
)


class TVimConfigGetter(IConfigGetter):
    def get_by_glob(self) -> Any:
        return self._get_vim_var("g:coderunner_by_glob")

    def get_by_file_ext(self) -> Any:
        return self._get_vim_var("g:coderunner_by_file_ext")

    def get_by_file_type(self) -> Any:
        return self._get_vim_var("g:coderunner_by_file_type")

    def get_dispatchers_order(self) -> Any:
        return self._get_vim_var("g:coderunner_runners_order")

    def get_executor(self) -> Any:
        return self._get_vim_var("g:coderunner_executor")

    def get_ignore_selection(self) -> Any:
        return self._get_vim_var("g:coderunner_ignore_selection")

    def get_respect_shebang(self) -> Any:
        return self._get_vim_var("g:coderunner_respect_shebang")

    def get_save_all_files_before_run(self) -> Any:
        return self._get_vim_var("g:coderunner_save_all_files_before_run")

    def get_save_file_before_run(self) -> Any:
        return self._get_vim_var("g:coderunner_save_file_before_run")

    def _get_vim_var(self, var_name: str) -> Any:
        try:
            return vim.eval(var_name)
        except vim.error:
            raise UndefinedValueError(f"Vim variable {var_name} is not defined. Please set it in your vimrc.")


class TVimConfigManager(TBasicConfigManager):
    by_glob_alias: ClassVar[str] = "g:coderunner_by_glob"
    by_file_ext_alias: ClassVar[str] = "g:coderunner_by_file_ext"
    by_file_type_alias: ClassVar[str] = "g:coderunner_by_file_type"

    dispatchers_order_alias: ClassVar[str] = "g:coderunner_runners_order"

    executor_alias: ClassVar[str] = "g:coderunner_executor"

    ignore_selection_alias: ClassVar[str] = "g:coderunner_ignore_selection"
    respect_shebang_alias: ClassVar[str] = "g:coderunner_respect_shebang"
    save_all_files_before_run_alias: ClassVar[str] = "g:coderunner_save_all_files_before_run"
    save_file_before_run_alias: ClassVar[str] = "g:coderunner_save_file_before_run"
