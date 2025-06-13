import glob
import re
from typing import Dict, Optional

from src.coderunner import TCodeRunner
from src.coderunner_builder.interface import ICodeRunnerBuilder
from src.command_builder import TInterpolatorCommandBuilder
from src.command_builders_dispatcher import (
    TFileExtCommandBuildersDispatcher,
    TFileTypeCommandBuildersDispatcher,
    TGlobCommandBuildersDispatcher,
    TShebangCommandBuildersDispatcher,
)
from src.command_dispatcher_strategy_selector import (
    TBasicCommandDispatcherStrategySelector,
)
from src.commands_executor import TVimCommandsExecutor
from src.config_manager import TVimConfigManager
from src.editor import TVimEditor
from src.editor_service_for_coderunner import TBasicEditorServiceForCodeRunner
from src.file_info_extractor import TBasicFileInfoExtractor
from src.message_printer import TVimMessagePrinter
from src.project_info_extractor import TVimProjectInfoExtractor


class TVimCodeRunnerBuilder(ICodeRunnerBuilder):
    def build(self) -> Optional[TCodeRunner]:
        config_manager: TVimConfigManager = TVimConfigManager()
        message_printer: TVimMessagePrinter = TVimMessagePrinter()

        try:
            file_info_extractor: TBasicFileInfoExtractor = TBasicFileInfoExtractor()
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
        file_info_extractor: TBasicFileInfoExtractor,
        project_info_extractor: TVimProjectInfoExtractor,
    ) -> TBasicCommandDispatcherStrategySelector:
        shebang_command_builders_dispatcher: TShebangCommandBuildersDispatcher = TShebangCommandBuildersDispatcher(
            file_info_extractor
        )
        glob_command_builders_dispatcher: TGlobCommandBuildersDispatcher = self._build_glob_command_builders_dispatcher(
            config_manager, file_info_extractor, project_info_extractor
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

        return TBasicCommandDispatcherStrategySelector(
            shebang_command_builders_dispatcher=shebang_command_builders_dispatcher,
            glob_command_builders_dispatcher=glob_command_builders_dispatcher,
            file_ext_command_builders_dispatcher=file_ext_command_builders_dispatcher,
            file_type_command_builders_dispatcher=file_type_command_builders_dispatcher,
            config_manager=config_manager,
        )

    def _build_glob_command_builders_dispatcher(
        self,
        config_manager: TVimConfigManager,
        file_info_extractor: TBasicFileInfoExtractor,
        project_info_extractor: TVimProjectInfoExtractor,
    ) -> TGlobCommandBuildersDispatcher:
        dict_with_commands: Dict[str, str] = config_manager.get_glob_to_command()
        return TGlobCommandBuildersDispatcher(
            tuple(
                (
                    re.compile(glob.translate(key, recursive=True, include_hidden=True)),
                    TInterpolatorCommandBuilder(dict_with_commands[key], project_info_extractor, file_info_extractor),
                )
                for key in sorted(dict_with_commands)
            )
        )

    def _build_file_ext_command_builders_dispatcher(
        self,
        config_manager: TVimConfigManager,
        file_info_extractor: TBasicFileInfoExtractor,
        project_info_extractor: TVimProjectInfoExtractor,
    ) -> TFileExtCommandBuildersDispatcher:
        return TFileExtCommandBuildersDispatcher(
            {
                key: TInterpolatorCommandBuilder(val, project_info_extractor, file_info_extractor)
                for key, val in config_manager.get_file_ext_to_command().items()
            },
            file_info_extractor,
        )

    def _build_file_type_command_builders_dispatcher(
        self,
        config_manager: TVimConfigManager,
        file_info_extractor: TBasicFileInfoExtractor,
        project_info_extractor: TVimProjectInfoExtractor,
    ) -> TFileTypeCommandBuildersDispatcher:
        return TFileTypeCommandBuildersDispatcher(
            {
                key: TInterpolatorCommandBuilder(val, project_info_extractor, file_info_extractor)
                for key, val in config_manager.get_file_type_to_command().items()
            },
            file_info_extractor,
        )
