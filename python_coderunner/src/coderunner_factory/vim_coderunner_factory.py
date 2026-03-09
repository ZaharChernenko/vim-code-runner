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
    EDispatchersTypes,
    TBasicCommandDispatcherStrategySelector,
)
from ..commands_executor import TVimCommandsExecutor
from ..config_manager import (
    ConfigField,
    TVimConfigGetter,
    TVimConfigManager,
    UndefinedValueError,
)
from ..editor import TVimEditor
from ..editor_service_for_coderunner import TBasicEditorServiceForCodeRunner
from ..file_info_extractor import TVimFileInfoExtractor
from ..message_printer import TVimMessagePrinter
from ..project_info_extractor import TVimProjectInfoExtractor
from ..validators import (
    TBoolValidator,
    TDispatchersOrderValidator,
    TDispatchersValidator,
    TStrValidator,
)
from .interface import ICodeRunnerFactory


class TVimCodeRunnerFactory(ICodeRunnerFactory):
    def create(self) -> Optional[TCodeRunner]:
        config_getter = TVimConfigGetter()
        config_manager = self._create_config_manager(config_getter)
        message_printer: TVimMessagePrinter = TVimMessagePrinter()

        try:
            file_info_extractor: TVimFileInfoExtractor = TVimFileInfoExtractor()
            project_info_extractor: TVimProjectInfoExtractor = TVimProjectInfoExtractor(file_info_extractor)

            editor: TVimEditor = TVimEditor()
            editor_service_for_coderunner: TBasicEditorServiceForCodeRunner = TBasicEditorServiceForCodeRunner(
                config_manager, editor, file_info_extractor
            )

            command_dispatcher_strategy_selector: TBasicCommandDispatcherStrategySelector = (
                self._create_command_dispatcher_strategy_selector(
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

        except (ValueError, UndefinedValueError) as e:
            message_printer.error(str(e))

        return None

    def _create_config_manager(self, config_getter: TVimConfigGetter) -> TVimConfigManager:
        """Creates TVimConfigManager with ConfigField objects"""
        config_manager = TVimConfigManager(
            by_file_ext_field=ConfigField(
                name="by_file_ext",
                getter=config_getter.get_by_file_ext,
                validator=TDispatchersValidator(),
                allowed_values_description="Dict[str, str] value",
            ),
            by_file_type_field=ConfigField(
                name="by_file_type",
                getter=config_getter.get_by_file_type,
                validator=TDispatchersValidator(),
                allowed_values_description="Dict[str, str] value",
            ),
            by_glob_field=ConfigField(
                name="by_glob",
                getter=config_getter.get_by_glob,
                validator=TDispatchersValidator(),
                allowed_values_description="Dict[str, str] value",
            ),
            dispatchers_order_field=ConfigField(
                name="runners_order",
                getter=config_getter.get_dispatchers_order,
                validator=TDispatchersOrderValidator(set(EDispatchersTypes)),
                allowed_values_description=", ".join(dispatcher_type.value for dispatcher_type in EDispatchersTypes),
            ),
            coderunner_tempfile_prefix_field=ConfigField(
                name="coderunner_tempfile_prefix",
                getter=config_getter.get_coderunner_tempfile_prefix,
                validator=TStrValidator(),
                allowed_values_description="str value",
            ),
            executor_field=ConfigField(
                name="executor",
                getter=config_getter.get_executor,
                validator=TStrValidator(),
                allowed_values_description="str value",
            ),
            ignore_selection_field=ConfigField(
                name="ignore_selection",
                getter=config_getter.get_ignore_selection,
                validator=TBoolValidator(),
                allowed_values_description="0 or 1",
            ),
            respect_shebang_field=ConfigField(
                name="respect_shebang",
                getter=config_getter.get_respect_shebang,
                validator=TBoolValidator(),
                allowed_values_description="0 or 1",
            ),
            remove_coderunner_tempfiles_on_exit_field=ConfigField(
                name="coderunner_remove_coderunner_tempfiles_on_exit",
                getter=config_getter.get_remove_coderunner_tempfiles_on_exit,
                validator=TBoolValidator(),
                allowed_values_description="0 or 1",
            ),
            save_all_files_before_run_field=ConfigField(
                name="save_all_files_before_run",
                getter=config_getter.get_save_all_files_before_run,
                validator=TBoolValidator(),
                allowed_values_description="0 or 1",
            ),
            save_file_before_run_field=ConfigField(
                name="save_file_before_run",
                getter=config_getter.get_save_file_before_run,
                validator=TBoolValidator(),
                allowed_values_description="0 or 1",
            ),
        )
        return config_manager

    def _create_command_dispatcher_strategy_selector(
        self,
        config_manager: TVimConfigManager,
        file_info_extractor: TVimFileInfoExtractor,
        project_info_extractor: TVimProjectInfoExtractor,
    ) -> TBasicCommandDispatcherStrategySelector:
        shebang_command_builders_dispatcher: TShebangCommandBuildersDispatcher = TShebangCommandBuildersDispatcher(
            file_info_extractor
        )
        file_ext_command_builders_dispatcher: TFileExtCommandBuildersDispatcher = (
            self._create_file_ext_command_builders_dispatcher(
                config_manager, file_info_extractor, project_info_extractor
            )
        )
        file_type_command_builders_dispatcher: TFileTypeCommandBuildersDispatcher = (
            self._create_file_type_command_builders_dispatcher(
                config_manager, file_info_extractor, project_info_extractor
            )
        )
        glob_command_builders_dispatcher: TGlobCommandBuildersDispatcher = (
            self._create_glob_command_builders_dispatcher(config_manager, file_info_extractor, project_info_extractor)
        )

        return TBasicCommandDispatcherStrategySelector(
            shebang_command_builders_dispatcher=shebang_command_builders_dispatcher,
            glob_command_builders_dispatcher=glob_command_builders_dispatcher,
            file_ext_command_builders_dispatcher=file_ext_command_builders_dispatcher,
            file_type_command_builders_dispatcher=file_type_command_builders_dispatcher,
            config_manager=config_manager,
        )

    def _create_file_ext_command_builders_dispatcher(
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

    def _create_file_type_command_builders_dispatcher(
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

    def _create_glob_command_builders_dispatcher(
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
