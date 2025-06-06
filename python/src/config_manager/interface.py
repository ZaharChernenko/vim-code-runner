from abc import ABC, abstractmethod
from enum import StrEnum


class EDispatchersTypes(StrEnum):
    BY_FILE_TYPE = "by_file_type"
    BY_FILE_EXT = "by_file_ext"
    BY_GLOB = "by_glob"


class IConfigManager(ABC):
    @abstractmethod
    def get_save_file(self) -> bool:
        raise NotImplementedError

    @abstractmethod
    def get_save_all_files(self) -> bool:
        raise NotImplementedError

    @abstractmethod
    def get_respect_shebang(self) -> bool:
        raise NotImplementedError

    @abstractmethod
    def get_dispatchers_order(self) -> list[EDispatchersTypes]:
        raise NotImplementedError
