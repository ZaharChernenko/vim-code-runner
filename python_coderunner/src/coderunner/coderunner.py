from typing import Callable, Optional

from src.command_builder import ICommandBuilder
from src.command_dispatcher_strategy_selector import (
    TBasicCommandDispatcherStrategySelector,
)
from src.commands_executor import ICommandsExecutor
from src.config_manager import TBasicConfigManager
from src.editor_service_for_coderunner import TBasicEditorServiceForCodeRunner
from src.message_printer import IMessagePrinter


class TCodeRunner:
    def __init__(
        self,
        *,
        config_manager: TBasicConfigManager,
        editor_service: TBasicEditorServiceForCodeRunner,
        command_dispatcher_strategy_selector: TBasicCommandDispatcherStrategySelector,
        commands_executor: ICommandsExecutor,
        message_printer: IMessagePrinter,
    ):
        self._config_manager: TBasicConfigManager = config_manager
        self._editor_service: TBasicEditorServiceForCodeRunner = editor_service
        self._command_dispatcher_strategy_selector: TBasicCommandDispatcherStrategySelector = (
            command_dispatcher_strategy_selector
        )
        self._commands_executor: ICommandsExecutor = commands_executor
        self._message_printer: IMessagePrinter = message_printer

    def run(self) -> None:
        self._run(self._command_dispatcher_strategy_selector.dispatch)

    def run_by_glob(self) -> None:
        self._run(self._command_dispatcher_strategy_selector.dispatch_by_glob)

    def run_by_file_ext(self) -> None:
        self._run(self._command_dispatcher_strategy_selector.dispatch_by_file_ext)

    def run_by_file_type(self) -> None:
        self._run(self._command_dispatcher_strategy_selector.dispatch_by_file_type)

    def _run(self, strategy: Callable[[str], Optional[ICommandBuilder]]) -> None:
        try:
            with self._editor_service.get_file_for_run() as file_path_abs:
                if (command_builder := strategy(file_path_abs)) is not None:
                    self._editor_service.prepare_for_run()
                    self._commands_executor.execute(command_builder.build(file_path_abs))
        except ValueError as e:
            self._message_printer.error(str(e))

    def remove_coderunner_tempfiles(self) -> None:
        self._editor_service.remove_coderunner_tempfiles()

    def on_exit(self) -> None:
        if self._config_manager.get_remove_coderunner_tempfiles_on_exit():
            self.remove_coderunner_tempfiles()
