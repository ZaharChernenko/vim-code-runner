import os
import typing

from .interface import ICompilingRunner


class TCppRunner(ICompilingRunner):
    BINARY_FILENAME: typing.Final[str] = "cpp_output"
    EXTENSIONS: typing.Final[typing.FrozenSet[str]] = frozenset(
        (".cpp", ".cxx", ".cc", ".c", ".m", ".mm", ".h", ".hxx", ".hpp", ".hh")
    )

    @classmethod
    def get_binary_filename(cls) -> str:
        return cls.BINARY_FILENAME

    @classmethod
    def get_extensions(cls) -> typing.FrozenSet[str]:
        return cls.EXTENSIONS

    @classmethod
    def run(cls, filepath: str) -> str:
        if cls.needs_recompile(os.path.dirname(filepath)):
            return f'ter sh -c "g++ -o {cls.get_binary_filename()} -std=c++2a *.cpp && ./{cls.get_binary_filename()}"'
        return f"ter ./{cls.get_binary_filename()}"
