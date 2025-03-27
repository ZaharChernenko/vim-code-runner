import os
import typing

from .interface import ICompilingRunner


class TCppRunner(ICompilingRunner):
    BINARY_FILE_PATH: typing.Final[str] = "cpp_output"
    EXTENSIONS: typing.Final[typing.FrozenSet[str]] = frozenset(
        (".cpp", ".cxx", ".cc", ".c", ".m", ".mm", ".h", ".hxx", ".hpp", ".hh")
    )

    @classmethod
    def getBinaryFileName(cls) -> str:
        return cls.BINARY_FILE_PATH

    @classmethod
    def getExtensions(cls) -> typing.FrozenSet[str]:
        return cls.EXTENSIONS

    @classmethod
    def run(cls, filepath: str) -> str:
        if cls.needsRecompile(os.path.dirname(filepath)):
            return f'ter sh -c "g++ -o {cls.getBinaryFileName()} -std=c++2a *.cpp && ./{cls.getBinaryFileName()}"'
        return f"ter ./{cls.getBinaryFileName()}"
