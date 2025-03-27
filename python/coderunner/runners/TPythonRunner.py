import os
import sys
import typing

from .interface import IRunner


class TPythonRunner(IRunner):
    DEFAULT_PYTHON3: typing.Final[str] = "python3-intel64" if sys.platform == "darwin" else "python3"
    FILENAME_TO_PYTHON3: dict[str, str] = {}
    VENV_NODES: typing.Final[tuple[str, ...]] = (".venv/bin/python3", "venv/bin/python3", "virtualenv/bin/python3")

    @classmethod
    def findPythonPathInCache(cls, filepath: str) -> typing.Optional[str]:
        return cls.FILENAME_TO_PYTHON3.get(filepath, None)

    @classmethod
    def findPythonPathInFilesystem(cls, source_directory_path: str) -> str:
        for node in cls.VENV_NODES:
            path: typing.Optional[str] = cls.findNodeUpwards(source_directory_path, node)
            if path is not None:
                return path
        return cls.DEFAULT_PYTHON3

    @classmethod
    def getPythonPath(cls, filepath: str) -> str:
        cache_path: typing.Optional[str] = cls.findPythonPathInCache(filepath)
        if cache_path is not None and (os.path.exists(cache_path) or cache_path == cls.DEFAULT_PYTHON3):
            return cache_path

        new_path: str = cls.findPythonPathInFilesystem(os.path.dirname(filepath))
        cls.FILENAME_TO_PYTHON3[filepath] = new_path

        return new_path

    @classmethod
    def run(cls, filepath: str):
        return f'ter "{cls.getPythonPath(filepath)}" "{filepath}"'
