import typing

import vim
from coderunner import decorators, metaclasses, runners


class TRunnerContext(metaclass=metaclasses.ContextMeta):
    LANG_TO_RUNNER: typing.Final[typing.Dict[str, typing.Type[runners.IRunner]]] = {
        "python": runners.TPythonRunner,
        "cpp": runners.TCppRunner,
    }

    @classmethod
    @decorators.save_file_if(vim.eval("g:coderunner_save_file_before_run"))
    @decorators.save_all_files_if(vim.eval("g:coderunner_save_all_files_before_run"))
    def run(cls, filetype: str, filepath: str):
        runner: typing.Optional[typing.Type[runners.IRunner]] = cls.LANG_TO_RUNNER.get(filetype)
        if runner is None:
            return
        vim.command(cls.LANG_TO_RUNNER[filetype].run(filepath))

    @classmethod
    def clear(cls):
        runners.TPythonRunner.clear()
