from contextlib import contextmanager
from tempfile import NamedTemporaryFile
from typing import Generator

from src.config_manager import IConfigManager
from src.editor import IEditor
from src.file_info_extractor import IFileInfoExtractor


class TBasicEditorServiceForCodeRunner:
    def __init__(self, config_manager: IConfigManager, editor: IEditor, file_info_extractor: IFileInfoExtractor):
        self._config_manager: IConfigManager = config_manager
        self._editor: IEditor = editor
        self._file_info_extractor: IFileInfoExtractor = file_info_extractor

    @contextmanager
    def get_file_for_run(self) -> Generator[str]:
        file_path_abs: str = self._editor.get_current_file_name()

        if (
            not self._config_manager.get_ignore_selection()
            and (selected_text := self._editor.get_selected_text()) is not None
        ):
            with NamedTemporaryFile(
                "w",
                encoding="utf-8",
                dir=self._file_info_extractor.get_dir(file_path_abs),
                suffix=self._file_info_extractor.get_file_ext(file_path_abs),
                delete=True,
            ) as temp_file:
                temp_file.write(selected_text)
                temp_file.flush()
                yield temp_file.name
        else:
            yield file_path_abs

    def prepare_for_run(self) -> None:
        if self._config_manager.get_save_all_files():
            self._editor.save_all_files()
            return
        if self._config_manager.get_save_file():
            self._editor.save_file()
            return
