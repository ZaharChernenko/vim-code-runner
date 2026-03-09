from typing import Optional

import vim

from .base import TBaseFileInfoExtractor


class TVimFileInfoExtractor(TBaseFileInfoExtractor):
    def get_file_type(self, file_path_abs: str) -> Optional[str]:
        file_type: Optional[str] = vim.eval("&filetype")
        return None if not file_type else file_type
