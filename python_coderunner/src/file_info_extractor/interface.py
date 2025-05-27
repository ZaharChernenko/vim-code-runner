import os
from abc import ABC, abstractmethod
from typing import Optional


class IFileInfoExtractor(ABC):
    """
    Declares all commands that are directly connected to the file.
    Accepts only file absolute path.
    """

    def get_dir(self, file_path_abs: str) -> str:
        dir_path: str = os.path.dirname(file_path_abs)
        if dir_path and not dir_path.endswith(os.sep):
            dir_path += os.sep
        return dir_path

    def get_dir_without_trailing_slash(self, file_path_abs: str) -> str:
        return os.path.dirname(file_path_abs).rstrip(os.sep)

    def get_drive_letter(self, file_path_abs: str) -> str:
        drive, _ = os.path.splitdrive(file_path_abs)
        return drive

    def get_file_ext(self, file_path_abs: str) -> str:
        base: str = self.get_file_name(file_path_abs)
        dot_pos: int = base.rfind(".")
        return base[dot_pos : len(base)].lower() if dot_pos != -1 else ""

    def get_file_name(self, file_path_abs: str) -> str:
        return os.path.basename(file_path_abs)

    def get_file_name_without_ext(self, file_path_abs: str) -> str:
        base: str = self.get_file_name(file_path_abs)
        dot_pos: int = base.rfind(".")
        return base[:dot_pos] if dot_pos != -1 else base

    @abstractmethod
    def get_file_type(self, file_path_abs: str) -> Optional[str]:
        raise NotImplementedError

    def get_shebang(self, file_path_abs: str) -> Optional[str]:
        if not os.path.exists(file_path_abs):
            return None

        try:
            with open(file_path_abs, "r", encoding="utf-8") as fin:
                first_line: str = fin.readline().strip()
                return first_line[2:] if first_line.startswith("#!") and not first_line.startswith("#![") else None
        except (IOError, UnicodeDecodeError):
            return None
