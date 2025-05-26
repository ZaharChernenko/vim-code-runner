from abc import ABC, abstractmethod
from enum import StrEnum


class ERunnersTypes(StrEnum):
    BY_FILE_TYPE = "by_file_type"
    BY_EXT = "by_ext"
    BY_GLOB = "by_glob"


class IConfigManager(ABC):
    @abstractmethod
    def get_save_file(self) -> bool:
        raise NotImplementedError

    @abstractmethod
    def get_save_all_files(self) -> bool:
        raise NotImplementedError

    @abstractmethod
    def get_runners_order(self) -> list[ERunnersTypes]:
        raise NotImplementedError
