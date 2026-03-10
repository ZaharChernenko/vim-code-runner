import glob
import re
import sys
import tempfile
import unittest
from typing import Generator
from unittest import mock
from unittest.mock import MagicMock

import pytest
from pytest_lazyfixture import lazy_fixture

sys.modules["vim"] = MagicMock()
from src.command_builder import ICommandBuilder
from src.command_builders_dispatcher import (
    TFileExtCommandBuildersDispatcher,
    TFileTypeCommandBuildersDispatcher,
    TGlobCommandBuildersDispatcher,
    TShebangCommandBuildersDispatcher,
)
from src.config import (
    EDispatchersTypes,
    IConfig,
    TConfigField,
    TVimConfig,
)
from src.config.getter import (
    IConfigValueGetter,
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
from src.config.validator import TBoolValidator, TDispatchersOrderValidator, TDispatchersValidator, TStrValidator
from src.file_info_extractor import (
    IFileInfoExtractor,
    TVimFileInfoExtractor,
)
from src.project_info_extractor import (
    IProjectInfoExtractor,
    TVimProjectInfoExtractor,
)


@pytest.fixture(params=(lazy_fixture("fixture_vim_config"),))
def fixture_config(request: pytest.FixtureRequest) -> IConfig:
    return request.param


@pytest.fixture
def fixture_vim_config() -> IConfig:
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


@pytest.fixture
def fixture_shebang_command_builders_dispatcher(
    fixture_file_info_extractor: IFileInfoExtractor,
) -> TShebangCommandBuildersDispatcher:
    return TShebangCommandBuildersDispatcher(fixture_file_info_extractor)


@pytest.fixture
def fixture_file_ext_command_builders_dispatcher(
    fixture_file_info_extractor: IFileInfoExtractor,
) -> TFileExtCommandBuildersDispatcher:
    extensions: tuple[str, ...] = (".py", ".js", ".ts", ".java", ".cpp", ".c", ".go", ".rb", ".txt", ".z")
    file_ext_to_builder: dict[str, ICommandBuilder] = {
        ext: MagicMock(spec=ICommandBuilder, build=MagicMock(return_value=ext)) for ext in extensions
    }

    return TFileExtCommandBuildersDispatcher(
        file_ext_to_builder=file_ext_to_builder, file_info_extractor=fixture_file_info_extractor
    )


@pytest.fixture
def fixture_file_type_command_builders_dispatcher(
    fixture_file_info_extractor: IFileInfoExtractor,
) -> TFileTypeCommandBuildersDispatcher:
    languages: tuple[str, ...] = (
        "python",
        "javascript",
        "typescript",
        "cpp",
    )
    file_type_to_builder: dict[str, ICommandBuilder] = {
        lang: MagicMock(spec=ICommandBuilder, build=MagicMock(return_value=lang)) for lang in languages
    }

    return TFileTypeCommandBuildersDispatcher(
        file_type_to_builder=file_type_to_builder, file_info_extractor=fixture_file_info_extractor
    )


@pytest.fixture
def fixture_glob_command_builders_dispatcher() -> TGlobCommandBuildersDispatcher:
    glob_patterns: tuple[str, ...] = (
        "**/*.py",
        "**/test.py",
        "*.js",
        "*.java",
        "*.cpp",
        "*.8xp.txt",
        "*.*.*",
        "**/*.log",
        "**/*.*.*",
    )
    glob_to_builder: tuple[tuple[re.Pattern, ICommandBuilder], ...] = tuple(
        (
            re.compile(glob.translate(pattern, recursive=True, include_hidden=True)),
            MagicMock(spec=ICommandBuilder, build=MagicMock(return_value=pattern)),
        )
        for pattern in sorted(glob_patterns, reverse=True)
    )

    return TGlobCommandBuildersDispatcher(glob_to_builder)


@pytest.fixture(params=(lazy_fixture("fixture_vim_project_info_extractor"),))
def fixture_project_info_extractor(request: pytest.FixtureRequest) -> IProjectInfoExtractor:
    return request.param


@pytest.fixture
def fixture_vim_project_info_extractor(
    fixture_file_info_extractor: IFileInfoExtractor,
) -> Generator[IProjectInfoExtractor, None, None]:
    with tempfile.TemporaryDirectory() as temp_dir:
        extractor: TVimProjectInfoExtractor = TVimProjectInfoExtractor(fixture_file_info_extractor)
        with mock.patch.object(
            extractor,
            "get_workspace_root",
            return_value=temp_dir,
        ):
            yield extractor


@pytest.fixture(params=(lazy_fixture("fixture_vim_file_info_extractor"),))
def fixture_file_info_extractor(request: pytest.FixtureRequest) -> IFileInfoExtractor:
    return request.param


@pytest.fixture
def fixture_vim_file_info_extractor() -> Generator[IFileInfoExtractor, None, None]:
    extractor: TVimFileInfoExtractor = TVimFileInfoExtractor()
    ext_to_lang: dict[str, str] = {
        ".py": "python",
        ".cpp": "cpp",
        ".rs": "rust",
        ".ts": "typescript",
        ".js": "javascript",
    }
    with mock.patch.object(
        extractor,
        "get_file_type",
        side_effect=lambda file_path_abs: ext_to_lang.get(extractor.get_file_ext(file_path_abs)),
    ):
        yield extractor
