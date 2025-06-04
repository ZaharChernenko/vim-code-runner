from src.command_builder.interface import ICommandBuilder


class TShebangCommandBuilder(ICommandBuilder):
    def __init__(self, shebang: str):
        self._shebang: str = shebang

    def build(self, file_path_abs: str) -> str:
        return f"{self._shebang} '{file_path_abs}'"
