import typing

import vim

from . import runners


class TRunnerContext:
    LANG_TO_RUNNER: typing.Final[typing.Dict[str, typing.Type[runners.IRunner]]] = {
        "python": runners.TPythonRunner,
        "cpp": runners.TCppRunner,
    }

    @classmethod
    def run(cls, filetype: str, filepath: str):
        runner: typing.Optional[typing.Type[runners.IRunner]] = cls.LANG_TO_RUNNER.get(filetype)
        if runner is None:
            return
        return vim.command(cls.LANG_TO_RUNNER[filetype].run(filepath))

    @classmethod
    def clear(cls):
        runners.TPythonRunner.clear()
