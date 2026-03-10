from abc import ABC, abstractmethod


class IEditor(ABC):
    @abstractmethod
    def get_current_file_name(self) -> str:
        raise NotImplementedError

    @abstractmethod
    def get_selected_text(self) -> str | None:
        raise NotImplementedError

    @abstractmethod
    def save_all_files(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def save_file(self) -> None:
        raise NotImplementedError
