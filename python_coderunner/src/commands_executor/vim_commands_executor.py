import vim

from ..config_manager import TBasicConfigManager
from .inteface import ICommandsExecutor


class TVimCommandsExecutor(ICommandsExecutor):
    def __init__(self, config_manager: TBasicConfigManager):
        self._config_manager: TBasicConfigManager = config_manager

    def execute(self, command: str) -> None:
        executor_command: str = self._config_manager.get_executor()
        vim.command(f"{executor_command} {command}")
