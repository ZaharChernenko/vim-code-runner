from abc import ABC, abstractmethod
from typing import Optional


class IEditor(ABC):
    @abstractmethod
    def get_current_file_name(self) -> str:
        raise NotImplementedError

    @abstractmethod
    def get_selected_text(self) -> Optional[str]:
        raise NotImplementedError

    @abstractmethod
    def save_all_file(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def save_file(self) -> None:
        raise NotImplementedError
