from abc import ABC, abstractmethod
from typing import Dict, List


class IConfigManager(ABC):
    """Интерфейс менеджера конфигурации"""

    @abstractmethod
    def get_by_file_ext(self) -> Dict[str, str]:
        """Получает конфиг для диспетчеризации по расширению файла"""
        raise NotImplementedError

    @abstractmethod
    def get_by_file_type(self) -> Dict[str, str]:
        """Получает конфиг для диспетчеризации по типу файла"""
        raise NotImplementedError

    @abstractmethod
    def get_by_glob(self) -> Dict[str, str]:
        """Получает конфиг для диспетчеризации по glob паттернам"""
        raise NotImplementedError

    @abstractmethod
    def get_dispatchers_order(self) -> List:
        """Получает порядок приоритета диспетчеров"""
        raise NotImplementedError

    @abstractmethod
    def get_coderunner_tempfile_prefix(self) -> str:
        """Получает префикс для временных файлов кодраннера"""
        raise NotImplementedError

    @abstractmethod
    def get_executor(self) -> str:
        """Получает исполнитель команд"""
        raise NotImplementedError

    @abstractmethod
    def get_ignore_selection(self) -> bool:
        """Получает флаг игнорирования выделения"""
        raise NotImplementedError

    @abstractmethod
    def get_respect_shebang(self) -> bool:
        """Получает флаг уважения shebang"""
        raise NotImplementedError

    @abstractmethod
    def get_remove_coderunner_tempfiles_on_exit(self) -> bool:
        """Получает флаг удаления временных файлов при выходе"""
        raise NotImplementedError

    @abstractmethod
    def get_save_all_files_before_run(self) -> bool:
        """Получает флаг сохранения всех файлов перед запуском"""
        raise NotImplementedError

    @abstractmethod
    def get_save_file_before_run(self) -> bool:
        """Получает флаг сохранения текущего файла перед запуском"""
        raise NotImplementedError
