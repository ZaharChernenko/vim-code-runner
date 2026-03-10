from abc import ABC, abstractmethod
from typing import Iterable


class IProjectInfoExtractor(ABC):
    @abstractmethod
    def get_workspace_root(self) -> str:
        raise NotImplementedError

    @abstractmethod
    def get_all_files_filter_by_exts(self, exts: set[str]) -> Iterable[str]:
        raise NotImplementedError

    @abstractmethod
    def get_all_files_filter_by_file_type(self, file_types: set[str]) -> Iterable[str]:
        raise NotImplementedError
