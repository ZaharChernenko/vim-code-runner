from typing import Optional

from src.command_builder import ICommandBuilder
from src.command_builders_dispatcher import (
    TFileExtCommandBuildersDispatcher,
    TFileTypeCommandBuildersDispatcher,
    TGlobCommandBuildersDispatcher,
    TShebangCommandBuildersDispatcher,
)
from src.config_manager import EDispatchersTypes, IConfigManager


class TBasicCommandDispatcherStrategySelector:
    def __init__(
        self,
        *,
        shebang_command_builders_dispatcher: TShebangCommandBuildersDispatcher,
        glob_command_builders_dispatcher: TGlobCommandBuildersDispatcher,
        file_ext_command_builders_dispatcher: TFileExtCommandBuildersDispatcher,
        file_type_command_builders_dispatcher: TFileTypeCommandBuildersDispatcher,
        config_manager: IConfigManager,
    ):
        self._shebang_command_builders_dispatcher: TShebangCommandBuildersDispatcher = (
            shebang_command_builders_dispatcher
        )
        self._glob_command_builders_dispatcher: TGlobCommandBuildersDispatcher = glob_command_builders_dispatcher
        self._file_ext_command_builders_dispatcher: TFileExtCommandBuildersDispatcher = (
            file_ext_command_builders_dispatcher
        )
        self._file_type_command_builders_dispatcher: TFileTypeCommandBuildersDispatcher = (
            file_type_command_builders_dispatcher
        )
        self._config_manager: IConfigManager = config_manager

    def dispatch_by_shebang(self, file_path_abs: str) -> Optional[ICommandBuilder]:
        return self._shebang_command_builders_dispatcher.dispatch(file_path_abs)

    def dispatch_by_glob(self, file_path_abs: str) -> Optional[ICommandBuilder]:
        return self._glob_command_builders_dispatcher.dispatch(file_path_abs)

    def dispatch_by_file_ext(self, file_path_abs: str) -> Optional[ICommandBuilder]:
        return self._file_ext_command_builders_dispatcher.dispatch(file_path_abs)

    def dispatch_by_file_type(self, file_path_abs: str) -> Optional[ICommandBuilder]:
        return self._file_type_command_builders_dispatcher.dispatch(file_path_abs)

    def dispatch(self, file_path_abs: str) -> Optional[ICommandBuilder]:
        command_builder: Optional[ICommandBuilder] = None

        if (
            self._config_manager.get_respect_shebang()
            and (command_builder := self.dispatch_by_shebang(file_path_abs)) is not None
        ):
            return command_builder

        for dispatcher in self._config_manager.get_dispatchers_order():
            if (
                dispatcher == EDispatchersTypes.BY_GLOB
                and (command_builder := self.dispatch_by_glob(file_path_abs)) is not None
            ):
                return command_builder
            if (
                dispatcher == EDispatchersTypes.BY_FILE_EXT
                and (command_builder := self.dispatch_by_file_ext(file_path_abs)) is not None
            ):
                return command_builder
            if (
                dispatcher == EDispatchersTypes.BY_FILE_TYPE
                and (command_builder := self.dispatch_by_file_type(file_path_abs)) is not None
            ):
                return command_builder

        return command_builder
