import abc
import typing


class IFileInfoExtractor(abc.ABC):
    """
    Declares all commands that are directly connected to the file.
    Accepts only file absolute path.
    """

    @abc.abstractmethod
    def get_workspace_root(self, file_path_abs: str) -> str:
        raise NotImplementedError

    @abc.abstractmethod
    def get_dir(self, file_path_abs: str) -> str:
        raise NotImplementedError

    @abc.abstractmethod
    def get_dir_without_trailing_slash(self, file_path_abs: str) -> str:
        raise NotImplementedError

    @abc.abstractmethod
    def get_file_name(self, file_path_abs: str) -> str:
        raise NotImplementedError

    @abc.abstractmethod
    def get_file_name_without_ext(self, file_path_abs: str) -> str:
        raise NotImplementedError

    @abc.abstractmethod
    def get_file_ext(self, file_path_abs: str) -> str:
        raise NotImplementedError

    @abc.abstractmethod
    def get_file_type(self, file_path_abs: str) -> typing.Optional[str]:
        raise NotImplementedError

    @abc.abstractmethod
    def get_full_file_name(self, file_path_abs: str) -> typing.Optional[str]:
        raise NotImplementedError

    @abc.abstractmethod
    def get_drive_letter(self, file_path_abs: str) -> str:
        raise NotImplementedError
