import vim

from ..config_manager import IConfigManager
from .inteface import ICommandsExecutor


class TVimCommandsExecutor(ICommandsExecutor):
    def __init__(self, config_manager: IConfigManager):
        self._config_manager: IConfigManager = config_manager

    def execute(self, command: str) -> None:
        executor_command: str = self._config_manager.get_executor()
        vim.command(f"{executor_command} {command}")
