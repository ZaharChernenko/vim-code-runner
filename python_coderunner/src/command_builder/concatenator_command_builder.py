from src.command_builder.interface import ICommandBuilder


class TConcatenatorCommandBuilder(ICommandBuilder):
    def __init__(self, command: str):
        self._command: str = command

    def build(self, file_path_abs: str) -> str:
        return f'{self._command} "{file_path_abs}"'
