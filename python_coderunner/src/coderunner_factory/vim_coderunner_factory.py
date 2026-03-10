import glob
import re

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
from ..config import EDispatchersTypes, TConfigField, TVimConfig
from ..config.getter import (
    TVimByFileExtConfigValueGetter,
    TVimByFileTypeConfigValueGetter,
    TVimByGlobConfigValueGetter,
    TVimCoderunnerTempfilePrefixConfigValueGetter,
    TVimDispatchersOrderConfigValueGetter,
    TVimExecutorConfigValueGetter,
    TVimIgnoreSelectionConfigValueGetter,
    TVimRemoveCoderunnerTempfilesOnExitConfigValueGetter,
    TVimRespectShebangConfigValueGetter,
    TVimSaveAllFilesBeforeRunConfigValueGetter,
    TVimSaveFileBeforeRunConfigValueGetter,
)
from ..config.validator import (
    TBoolValidator,
    TDispatchersOrderValidator,
    TDispatchersValidator,
    TStrValidator,
)
from ..editor import TVimEditor
from ..editor_service_for_coderunner import TBasicEditorServiceForCodeRunner
from ..file_info_extractor import TVimFileInfoExtractor
from ..message_printer import TVimMessagePrinter
from ..project_info_extractor import TVimProjectInfoExtractor
from .interface import ICodeRunnerFactory


class TVimCodeRunnerFactory(ICodeRunnerFactory):
    def create(self) -> TCodeRunner | None:
        config: TVimConfig = self._create_config()
        message_printer: TVimMessagePrinter = TVimMessagePrinter()

        try:
            file_info_extractor: TVimFileInfoExtractor = TVimFileInfoExtractor()
            project_info_extractor: TVimProjectInfoExtractor = TVimProjectInfoExtractor(file_info_extractor)

            editor: TVimEditor = TVimEditor()
            editor_service_for_coderunner: TBasicEditorServiceForCodeRunner = TBasicEditorServiceForCodeRunner(
                config, editor, file_info_extractor
            )

            command_dispatcher_strategy_selector: TBasicCommandDispatcherStrategySelector = (
                self._create_command_dispatcher_strategy_selector(config, file_info_extractor, project_info_extractor)
            )
            commands_executor: TVimCommandsExecutor = TVimCommandsExecutor(config)

            return TCodeRunner(
                config=config,
                editor_service=editor_service_for_coderunner,
                command_dispatcher_strategy_selector=command_dispatcher_strategy_selector,
                commands_executor=commands_executor,
                message_printer=message_printer,
            )

        except ValueError as e:
            message_printer.error(str(e))

        return None

    def _create_config(self) -> TVimConfig:
        return TVimConfig(
            by_file_ext_field=TConfigField(
                name="g:coderunner_by_file_ext",
                getter=TVimByFileExtConfigValueGetter(),
                validator=TDispatchersValidator(),
                allowed_values_description="Dict[str, str] value",
            ),
            by_file_type_field=TConfigField(
                name="g:coderunner_by_file_type",
                getter=TVimByFileTypeConfigValueGetter(),
                validator=TDispatchersValidator(),
                allowed_values_description="Dict[str, str] value",
            ),
            by_glob_field=TConfigField(
                name="g:coderunner_by_glob",
                getter=TVimByGlobConfigValueGetter(),
                validator=TDispatchersValidator(),
                allowed_values_description="Dict[str, str] value",
            ),
            dispatchers_order_field=TConfigField(
                name="g:coderunner_runners_order",
                getter=TVimDispatchersOrderConfigValueGetter(),
                validator=TDispatchersOrderValidator(),
                allowed_values_description=", ".join(dispatcher_type.value for dispatcher_type in EDispatchersTypes),
            ),
            coderunner_tempfile_prefix_field=TConfigField(
                name="g:coderunner_tempfile_prefix",
                getter=TVimCoderunnerTempfilePrefixConfigValueGetter(),
                validator=TStrValidator(),
                allowed_values_description="str value",
            ),
            executor_field=TConfigField(
                name="g:coderunner_executor",
                getter=TVimExecutorConfigValueGetter(),
                validator=TStrValidator(),
                allowed_values_description="str value",
            ),
            ignore_selection_field=TConfigField(
                name="g:coderunner_ignore_selection",
                getter=TVimIgnoreSelectionConfigValueGetter(),
                validator=TBoolValidator(),
                allowed_values_description="0 or 1",
            ),
            respect_shebang_field=TConfigField(
                name="g:coderunner_respect_shebang",
                getter=TVimRespectShebangConfigValueGetter(),
                validator=TBoolValidator(),
                allowed_values_description="0 or 1",
            ),
            remove_coderunner_tempfiles_on_exit_field=TConfigField(
                name="g:coderunner_remove_coderunner_tempfiles_on_exit",
                getter=TVimRemoveCoderunnerTempfilesOnExitConfigValueGetter(),
                validator=TBoolValidator(),
                allowed_values_description="0 or 1",
            ),
            save_all_files_before_run_field=TConfigField(
                name="g:coderunner_save_all_files_before_run",
                getter=TVimSaveAllFilesBeforeRunConfigValueGetter(),
                validator=TBoolValidator(),
                allowed_values_description="0 or 1",
            ),
            save_file_before_run_field=TConfigField(
                name="g:coderunner_save_file_before_run",
                getter=TVimSaveFileBeforeRunConfigValueGetter(),
                validator=TBoolValidator(),
                allowed_values_description="0 or 1",
            ),
        )

    def _create_command_dispatcher_strategy_selector(
        self,
        config: TVimConfig,
        file_info_extractor: TVimFileInfoExtractor,
        project_info_extractor: TVimProjectInfoExtractor,
    ) -> TBasicCommandDispatcherStrategySelector:
        shebang_command_builders_dispatcher: TShebangCommandBuildersDispatcher = TShebangCommandBuildersDispatcher(
            file_info_extractor
        )
        file_ext_command_builders_dispatcher: TFileExtCommandBuildersDispatcher = (
            self._create_file_ext_command_builders_dispatcher(config, file_info_extractor, project_info_extractor)
        )
        file_type_command_builders_dispatcher: TFileTypeCommandBuildersDispatcher = (
            self._create_file_type_command_builders_dispatcher(config, file_info_extractor, project_info_extractor)
        )
        glob_command_builders_dispatcher: TGlobCommandBuildersDispatcher = (
            self._create_glob_command_builders_dispatcher(config, file_info_extractor, project_info_extractor)
        )

        return TBasicCommandDispatcherStrategySelector(
            config=config,
            shebang_command_builders_dispatcher=shebang_command_builders_dispatcher,
            glob_command_builders_dispatcher=glob_command_builders_dispatcher,
            file_ext_command_builders_dispatcher=file_ext_command_builders_dispatcher,
            file_type_command_builders_dispatcher=file_type_command_builders_dispatcher,
        )

    def _create_file_ext_command_builders_dispatcher(
        self,
        config: TVimConfig,
        file_info_extractor: TVimFileInfoExtractor,
        project_info_extractor: TVimProjectInfoExtractor,
    ) -> TFileExtCommandBuildersDispatcher:
        return TFileExtCommandBuildersDispatcher(
            {
                key: TInterpolatorCommandBuilder(val, project_info_extractor, file_info_extractor)
                for key, val in config.get_by_file_ext().items()
            },
            file_info_extractor,
        )

    def _create_file_type_command_builders_dispatcher(
        self,
        config: TVimConfig,
        file_info_extractor: TVimFileInfoExtractor,
        project_info_extractor: TVimProjectInfoExtractor,
    ) -> TFileTypeCommandBuildersDispatcher:
        return TFileTypeCommandBuildersDispatcher(
            {
                key: TInterpolatorCommandBuilder(val, project_info_extractor, file_info_extractor)
                for key, val in config.get_by_file_type().items()
            },
            file_info_extractor,
        )

    def _create_glob_command_builders_dispatcher(
        self,
        config: TVimConfig,
        file_info_extractor: TVimFileInfoExtractor,
        project_info_extractor: TVimProjectInfoExtractor,
    ) -> TGlobCommandBuildersDispatcher:
        dict_with_commands: dict[str, str] = config.get_by_glob()
        return TGlobCommandBuildersDispatcher(
            tuple(
                (
                    re.compile(glob.translate(key, recursive=True, include_hidden=True)),
                    TInterpolatorCommandBuilder(dict_with_commands[key], project_info_extractor, file_info_extractor),
                )
                for key in sorted(dict_with_commands, reverse=True)
            )
        )
