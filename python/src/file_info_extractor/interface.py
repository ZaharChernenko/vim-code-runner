from abc import ABC, abstractmethod
from typing import Optional


class IFileInfoExtractor(ABC):
    """
    Declares all commands that are directly connected to the file.
    Accepts only file absolute path.
    """

    @abstractmethod
    def get_dir(self, file_path_abs: str) -> str:
        raise NotImplementedError

    @abstractmethod
    def get_dir_without_trailing_slash(self, file_path_abs: str) -> str:
        raise NotImplementedError

    @abstractmethod
    def get_file_name(self, file_path_abs: str) -> str:
        raise NotImplementedError

    @abstractmethod
    def get_file_name_without_ext(self, file_path_abs: str) -> str:
        raise NotImplementedError

    @abstractmethod
    def get_file_ext(self, file_path_abs: str) -> str:
        raise NotImplementedError

    @abstractmethod
    def get_file_type(self, file_path_abs: str) -> Optional[str]:
        raise NotImplementedError

    @abstractmethod
    def get_full_file_name(self, file_path_abs: str) -> Optional[str]:
        raise NotImplementedError

    @abstractmethod
    def get_drive_letter(self, file_path_abs: str) -> str:
        raise NotImplementedError

    @abstractmethod
    def get_shebang(self, file_path_abs: str) -> Optional[str]:
        raise NotImplementedError
