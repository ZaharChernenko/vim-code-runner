import vim

from src.project_info_extractor.interface import IProjectInfoExtractor


class TVimProjectInfoExtractor(IProjectInfoExtractor):
    def get_workspace_root(self) -> str:
        return vim.eval("getcwd()")
