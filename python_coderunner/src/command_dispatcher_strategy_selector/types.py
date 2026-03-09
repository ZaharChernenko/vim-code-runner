from enum import StrEnum


class EDispatchersTypes(StrEnum):
    BY_FILE_EXT = "by_file_ext"
    BY_FILE_TYPE = "by_file_type"
    BY_GLOB = "by_glob"
