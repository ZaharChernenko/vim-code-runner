import vim

from .interface import IProjectInfoExtractor


class TVimProjectInfoExtractor(IProjectInfoExtractor):
    def get_workspace_root(self) -> str:
        return vim.eval("getcwd()")
