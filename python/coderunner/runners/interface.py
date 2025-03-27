import abc
import os
import typing


class IRunner(abc.ABC):
    @classmethod
    @abc.abstractmethod
    def run(cls, filepath: str) -> str:
        raise NotImplementedError()

    @staticmethod
    def findNodeUpwards(source_path: str, node: str) -> typing.Optional[str]:
        """
        Searches for the desired node in the source_path directory and all ancestors
        """
        current_dir, next_dir = source_path, os.path.dirname(source_path)
        while current_dir != next_dir:  # until we reach the root
            path_to_node = os.path.join(current_dir, node)
            if os.path.exists(path_to_node):
                return path_to_node
            current_dir = next_dir  # going up
            next_dir = os.path.dirname(current_dir)
        return None
