from typing import Any

import vim

from src.config_manager.interface import EDispatchersTypes, IConfigManager


class TVimConfigManager(IConfigManager):
    def _get_executor_impl(self) -> str:
        return self._get_vim_var("g:coderunner_executor")

    def _get_save_file_impl(self) -> bool:
        return self._get_vim_var("g:coderunner_save_file_before_run")

    def _get_save_all_files_impl(self) -> bool:
        return self._get_vim_var("g:coderunner_save_all_files_before_run")

    def _get_respect_shebang_impl(self) -> bool:
        return self._get_vim_var("g:coderunner_respect_shebang")

    def _get_dispatchers_order_impl(self) -> list[EDispatchersTypes]:
        return self._get_vim_var("g:coderunner_runners_order")

    def _get_vim_var(self, var_name: str) -> Any:
        try:
            return vim.eval(var_name)
        except vim.error:
            raise ValueError(f"Vim variable {var_name} is not defined. Please set it in your vimrc.")
