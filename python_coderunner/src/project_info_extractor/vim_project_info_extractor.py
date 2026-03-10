import vim

from .base import TBaseProjectInfoExtractor


class TVimProjectInfoExtractor(TBaseProjectInfoExtractor):
    def get_workspace_root(self) -> str:
        return vim.eval("getcwd()")
