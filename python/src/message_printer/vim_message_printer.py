import vim

from src.message_printer.interface import IMessagePrinter


class TVimMessagePrinter(IMessagePrinter):
    def error(self, text: str) -> None:
        vim.command("echohl WarningMsg")
        for line in text.split("\n"):
            vim.command(f'echo "{self._escape_string(line)}"')
        vim.command("echohl None")

    def info(self, text: str) -> None:
        for line in text.split("\n"):
            vim.command(f'echo "{self._escape_string(line)}"')

    def _escape_string(self, text: str) -> str:
        return text.replace("\\", r"\\").replace('"', r"\"").replace("'", r"\'")
