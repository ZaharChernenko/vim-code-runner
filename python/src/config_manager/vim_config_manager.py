import vim

from src.config_manager.interface import ERunnersTypes, IConfigManager


class TVimConfigManager(IConfigManager):
    def get_save_file(self) -> bool:
        return vim.eval("g:coderunner_save_file_before_run")

    def get_save_all_files(self) -> bool:
        return vim.eval("g:coderunner_save_all_files_before_run")

    def get_runners_order(self) -> list[ERunnersTypes]:
        return vim.eval("g:coderunner_runners_order")
