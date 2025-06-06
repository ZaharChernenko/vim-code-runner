import vim

from src.config_manager.interface import EDispatchersTypes, IConfigManager


class TVimConfigManager(IConfigManager):
    def get_save_file(self) -> bool:
        return vim.eval("g:coderunner_save_file_before_run")

    def get_save_all_files(self) -> bool:
        return vim.eval("g:coderunner_save_all_files_before_run")

    def get_dispatchers_order(self) -> list[EDispatchersTypes]:
        return vim.eval("g:coderunner_runners_order")
