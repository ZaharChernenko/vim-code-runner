from typing import Optional

import vim

from src.editor.interface import IEditor


class TVimEditor(IEditor):
    def get_current_file_name(self) -> str:
        return vim.current.buffer.name

    def get_selected_text(self) -> Optional[str]:
        return vim.eval("coderunner#GetSelectedText()")

    def save_all_file(self) -> None:
        vim.command("wa")

    def save_file(self) -> None:
        vim.command("w")
