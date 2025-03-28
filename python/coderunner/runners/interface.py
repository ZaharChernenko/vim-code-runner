import abc
import os
import typing


class IRunner(abc.ABC):
    """Abstract base class for runners."""

    @classmethod
    @abc.abstractmethod
    def run(cls, filepath: str) -> str:
        raise NotImplementedError()

    @staticmethod
    def find_node_upwards(source_dir_path: str, node: str) -> typing.Optional[str]:
        """Searches for the desired node in the source directory and all ancestors"""

        current_dir, next_dir = source_dir_path, os.path.dirname(source_dir_path)
        while current_dir != next_dir:  # stop when we reach the root directory
            path_to_node = os.path.join(current_dir, node)
            if os.path.exists(path_to_node):
                return path_to_node
            current_dir = next_dir  # going up
            next_dir = os.path.dirname(current_dir)
        return None


class ICompilingRunner(IRunner, abc.ABC):
    """Abstract base class for runners that require compilation."""

    @classmethod
    @abc.abstractmethod
    def get_binary_filename(cls) -> str:
        raise NotImplementedError()

    @classmethod
    @abc.abstractmethod
    def get_extensions(cls) -> typing.FrozenSet[str]:
        raise NotImplementedError()

    @classmethod
    def needs_recompile(cls, source_dir_path: str) -> bool:
        """Check if recompilation is needed by comparing modification times"""

        binary_file_path: str = os.path.join(source_dir_path, cls.get_binary_filename())
        if not os.path.exists(binary_file_path):
            return True

        binary_file_modification_time: float = os.path.getmtime(binary_file_path)
        extensions: typing.FrozenSet[str] = cls.get_extensions()

        with os.scandir(source_dir_path) as nodes:
            for node in nodes:
                if not (node.is_file() and os.path.splitext(node.name)[1].lower() in extensions):
                    continue

                if os.path.getmtime(node.path) > binary_file_modification_time:
                    return True

        return False
