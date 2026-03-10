from abc import ABC, abstractmethod
from enum import StrEnum


class EDispatchersTypes(StrEnum):
    BY_FILE_EXT = "by_file_ext"
    BY_FILE_TYPE = "by_file_type"
    BY_GLOB = "by_glob"


class IConfig(ABC):
    @abstractmethod
    def get_by_file_ext(self) -> dict[str, str]:
        """Gets config for file extension-based dispatching"""
        raise NotImplementedError

    @abstractmethod
    def get_by_file_type(self) -> dict[str, str]:
        """Gets config for file type-based dispatching"""
        raise NotImplementedError

    @abstractmethod
    def get_by_glob(self) -> dict[str, str]:
        """Gets config for glob pattern-based dispatching"""
        raise NotImplementedError

    @abstractmethod
    def get_dispatchers_order(self) -> list[EDispatchersTypes]:
        """Gets the priority order of dispatchers"""
        raise NotImplementedError

    @abstractmethod
    def get_coderunner_tempfile_prefix(self) -> str:
        """Gets the prefix for coderunner temporary files"""
        raise NotImplementedError

    @abstractmethod
    def get_executor(self) -> str:
        """Gets the command executor"""
        raise NotImplementedError

    @abstractmethod
    def get_ignore_selection(self) -> bool:
        """Gets the flag for ignoring selection"""
        raise NotImplementedError

    @abstractmethod
    def get_respect_shebang(self) -> bool:
        """Gets the flag for respecting shebang"""
        raise NotImplementedError

    @abstractmethod
    def get_remove_coderunner_tempfiles_on_exit(self) -> bool:
        """Gets the flag for removing temporary files on exit"""
        raise NotImplementedError

    @abstractmethod
    def get_save_all_files_before_run(self) -> bool:
        """Gets the flag for saving all files before run"""
        raise NotImplementedError

    @abstractmethod
    def get_save_file_before_run(self) -> bool:
        """Gets the flag for saving current file before run"""
        raise NotImplementedError
