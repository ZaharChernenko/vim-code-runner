import vim

from ..config import IConfig
from .inteface import ICommandsExecutor


class TVimCommandsExecutor(ICommandsExecutor):
    def __init__(self, config: IConfig):
        self._config: IConfig = config

    def execute(self, command: str) -> None:
        executor_command: str = self._config.get_executor()
        vim.command(f"{executor_command} {command}")
