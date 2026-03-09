from typing import Any

import vim

from .basic import IConfigGetter, TBasicConfigManager, UndefinedValueError


class TVimConfigGetter(IConfigGetter):
    """Gets config values from Vim variables"""

    def get_by_file_ext(self) -> Any:
        return self._get_vim_var("g:coderunner_by_file_ext")

    def get_by_file_type(self) -> Any:
        return self._get_vim_var("g:coderunner_by_file_type")

    def get_by_glob(self) -> Any:
        return self._get_vim_var("g:coderunner_by_glob")

    def get_coderunner_tempfile_prefix(self) -> Any:
        return self._get_vim_var("g:coderunner_tempfile_prefix")

    def get_dispatchers_order(self) -> Any:
        return self._get_vim_var("g:coderunner_runners_order")

    def get_executor(self) -> Any:
        return self._get_vim_var("g:coderunner_executor")

    def get_ignore_selection(self) -> Any:
        return self._get_vim_var("g:coderunner_ignore_selection")

    def get_respect_shebang(self) -> Any:
        return self._get_vim_var("g:coderunner_respect_shebang")

    def get_remove_coderunner_tempfiles_on_exit(self) -> Any:
        return self._get_vim_var("g:coderunner_remove_coderunner_tempfiles_on_exit")

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
    """Config Manager for Vim, created through factory"""
