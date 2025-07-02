import os
from abc import ABC, abstractmethod
from typing import Iterable, Set

from ..file_info_extractor import IFileInfoExtractor


class IProjectInfoExtractor(ABC):
    def __init__(self, file_info_extractor: IFileInfoExtractor):
        self._file_info_extractor = file_info_extractor

    @abstractmethod
    def get_workspace_root(self) -> str:
        raise NotImplementedError

    def get_all_files_filter_by_exts(self, exts: Set[str]) -> Iterable[str]:
        for root, _, files in os.walk(self.get_workspace_root()):
            for file in files:
                if self._file_info_extractor.get_file_ext(file) in exts:
                    yield os.path.join(root, file)

    def get_all_files_filter_by_file_type(self, file_types: Set[str]) -> Iterable[str]:
        for root, _, files in os.walk(self.get_workspace_root()):
            for file in files:
                if self._file_info_extractor.get_file_type(file) in file_types:
                    yield os.path.join(root, file)
