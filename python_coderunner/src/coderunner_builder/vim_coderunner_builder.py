import glob
import re
from typing import Dict, Optional

from ..coderunner import TCodeRunner
from ..command_builder import TInterpolatorCommandBuilder
from ..command_builders_dispatcher import (
    TFileExtCommandBuildersDispatcher,
    TFileTypeCommandBuildersDispatcher,
    TGlobCommandBuildersDispatcher,
    TShebangCommandBuildersDispatcher,
)
from ..command_dispatcher_strategy_selector import (
    TBasicCommandDispatcherStrategySelector,
)
from ..commands_executor import TVimCommandsExecutor
from ..config_manager import (
    TBasicConfigValidator,
    TVimConfigGetter,
    TVimConfigManager,
)
from ..editor import TVimEditor
from ..editor_service_for_coderunner import TBasicEditorServiceForCodeRunner
from ..file_info_extractor import TVimFileInfoExtractor
from ..message_printer import TVimMessagePrinter
from ..project_info_extractor import TVimProjectInfoExtractor
from .interface import ICodeRunnerBuilder


class TVimCodeRunnerBuilder(ICodeRunnerBuilder):
    def build(self) -> Optional[TCodeRunner]:
        config_manager: TVimConfigManager = TVimConfigManager(TVimConfigGetter(), TBasicConfigValidator())
        message_printer: TVimMessagePrinter = TVimMessagePrinter()

        try:
            file_info_extractor: TVimFileInfoExtractor = TVimFileInfoExtractor()
            project_info_extractor: TVimProjectInfoExtractor = TVimProjectInfoExtractor(file_info_extractor)

            editor: TVimEditor = TVimEditor()
            editor_service_for_coderunner: TBasicEditorServiceForCodeRunner = TBasicEditorServiceForCodeRunner(
                config_manager, editor, file_info_extractor
            )

            command_dispatcher_strategy_selector: TBasicCommandDispatcherStrategySelector = (
                self._build_command_dispatcher_strategy_selector(
                    config_manager, file_info_extractor, project_info_extractor
                )
            )
            commands_executor: TVimCommandsExecutor = TVimCommandsExecutor(config_manager)

            return TCodeRunner(
                config_manager=config_manager,
                editor_service=editor_service_for_coderunner,
                command_dispatcher_strategy_selector=command_dispatcher_strategy_selector,
                commands_executor=commands_executor,
                message_printer=message_printer,
            )

        except ValueError as e:
            message_printer.error(str(e))

        return None

    def _build_command_dispatcher_strategy_selector(
        self,
        config_manager: TVimConfigManager,
        file_info_extractor: TVimFileInfoExtractor,
        project_info_extractor: TVimProjectInfoExtractor,
    ) -> TBasicCommandDispatcherStrategySelector:
        shebang_command_builders_dispatcher: TShebangCommandBuildersDispatcher = TShebangCommandBuildersDispatcher(
            file_info_extractor
        )
        file_ext_command_builders_dispatcher: TFileExtCommandBuildersDispatcher = (
            self._build_file_ext_command_builders_dispatcher(
                config_manager, file_info_extractor, project_info_extractor
            )
        )
        file_type_command_builders_dispatcher: TFileTypeCommandBuildersDispatcher = (
            self._build_file_type_command_builders_dispatcher(
                config_manager, file_info_extractor, project_info_extractor
            )
        )
        glob_command_builders_dispatcher: TGlobCommandBuildersDispatcher = self._build_glob_command_builders_dispatcher(
            config_manager, file_info_extractor, project_info_extractor
        )

        return TBasicCommandDispatcherStrategySelector(
            shebang_command_builders_dispatcher=shebang_command_builders_dispatcher,
            glob_command_builders_dispatcher=glob_command_builders_dispatcher,
            file_ext_command_builders_dispatcher=file_ext_command_builders_dispatcher,
            file_type_command_builders_dispatcher=file_type_command_builders_dispatcher,
            config_manager=config_manager,
        )

    def _build_file_ext_command_builders_dispatcher(
        self,
        config_manager: TVimConfigManager,
        file_info_extractor: TVimFileInfoExtractor,
        project_info_extractor: TVimProjectInfoExtractor,
    ) -> TFileExtCommandBuildersDispatcher:
        return TFileExtCommandBuildersDispatcher(
            {
                key: TInterpolatorCommandBuilder(val, project_info_extractor, file_info_extractor)
                for key, val in config_manager.get_by_file_ext().items()
            },
            file_info_extractor,
        )

    def _build_file_type_command_builders_dispatcher(
        self,
        config_manager: TVimConfigManager,
        file_info_extractor: TVimFileInfoExtractor,
        project_info_extractor: TVimProjectInfoExtractor,
    ) -> TFileTypeCommandBuildersDispatcher:
        return TFileTypeCommandBuildersDispatcher(
            {
                key: TInterpolatorCommandBuilder(val, project_info_extractor, file_info_extractor)
                for key, val in config_manager.get_by_file_type().items()
            },
            file_info_extractor,
        )

    def _build_glob_command_builders_dispatcher(
        self,
        config_manager: TVimConfigManager,
        file_info_extractor: TVimFileInfoExtractor,
        project_info_extractor: TVimProjectInfoExtractor,
    ) -> TGlobCommandBuildersDispatcher:
        dict_with_commands: Dict[str, str] = config_manager.get_by_glob()
        return TGlobCommandBuildersDispatcher(
            tuple(
                (
                    re.compile(glob.translate(key, recursive=True, include_hidden=True)),
                    TInterpolatorCommandBuilder(dict_with_commands[key], project_info_extractor, file_info_extractor),
                )
                for key in sorted(dict_with_commands, reverse=True)
            )
        )
