import vim

from ..config_manager import IConfig
from .inteface import ICommandsExecutor


class TVimCommandsExecutor(ICommandsExecutor):
    def __init__(self, config_manager: IConfig):
        self._config_manager: IConfig = config_manager

    def execute(self, command: str) -> None:
        executor_command: str = self._config_manager.get_executor()
        vim.command(f"{executor_command} {command}")
