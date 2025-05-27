from typing import Optional

import vim

from .interface import IEditor


class TVimEditor(IEditor):
    def get_current_file_name(self) -> str:
        return vim.current.buffer.name

    def get_selected_text(self) -> Optional[str]:
        return vim.eval("coderunner#GetSelectedText(a:visualmode, a:range, a:first_line, a:last_line)")

    def save_all_files(self) -> None:
        vim.command("wa")

    def save_file(self) -> None:
        vim.command("w")
