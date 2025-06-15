from contextlib import nullcontext as does_not_raise

import pytest
import pytest_mock

from src.config_manager import EDispatchersTypes, TBasicConfigManager


@pytest.mark.parametrize(
    ("content", "expected", "expectation"),
    (
        (
            {"*.py": "python", "*.js": "node"},
            {"*.py": "python", "*.js": "node"},
            does_not_raise(),
        ),
        ({"*.py": "python"}, {"*.py": "python"}, does_not_raise()),
        ("invalid", None, pytest.raises(ValueError)),
        (123, None, pytest.raises(ValueError)),
        (None, None, pytest.raises(ValueError)),
        ({"*.py": 123}, None, pytest.raises(ValueError)),
        ({123: "python"}, None, pytest.raises(ValueError)),
    ),
)
def test_get_dict_with_commands(
    fixture_config_manager: TBasicConfigManager,
    content,
    expected,
    expectation,
    mocker: pytest_mock.MockFixture,
):
    mocker.patch.object(fixture_config_manager._config_getter, "get_by_glob", return_value=content)
    mocker.patch.object(fixture_config_manager._config_getter, "get_by_file_ext", return_value=content)
    mocker.patch.object(fixture_config_manager._config_getter, "get_by_file_type", return_value=content)
    for dispatcher_getter in (
        fixture_config_manager.get_by_glob,
        fixture_config_manager.get_by_file_ext,
        fixture_config_manager.get_by_file_type,
    ):
        with expectation:
            result = dispatcher_getter()
            if expected is not None:
                assert result == expected


@pytest.mark.parametrize(
    ("content", "expected", "expectation"),
    (
        ([EDispatchersTypes.BY_GLOB], [EDispatchersTypes.BY_GLOB], does_not_raise()),
        (
            [EDispatchersTypes.BY_FILE_EXT, EDispatchersTypes.BY_GLOB],
            [EDispatchersTypes.BY_FILE_EXT, EDispatchersTypes.BY_GLOB],
            does_not_raise(),
        ),
        (["invalid"], None, pytest.raises(ValueError)),
        ([1], None, pytest.raises(ValueError)),
        ({}, None, pytest.raises(ValueError)),
    ),
)
def test_get_dispatchers_order(
    fixture_config_manager: TBasicConfigManager, content, expected, expectation, mocker: pytest_mock.MockFixture
):
    mocker.patch.object(fixture_config_manager._config_getter, "get_dispatchers_order", return_value=content)
    with expectation:
        result: list[EDispatchersTypes] = fixture_config_manager.get_dispatchers_order()
    if expected is not None:
        assert result == expected


@pytest.mark.parametrize(
    ("content", "expected", "expectation"),
    (
        (True, True, does_not_raise()),
        (False, False, does_not_raise()),
        ("1", True, does_not_raise()),
        ("0", False, does_not_raise()),
        (1, True, does_not_raise()),
        (0, False, does_not_raise()),
        ("invalid", None, pytest.raises(ValueError)),
        (None, None, pytest.raises(ValueError)),
    ),
)
def test_get_ignore_selection(
    fixture_config_manager: TBasicConfigManager,
    content,
    expected,
    expectation,
    mocker: pytest_mock.MockFixture,
):
    mocker.patch.object(fixture_config_manager._config_getter, "get_ignore_selection", return_value=content)
    mocker.patch.object(fixture_config_manager._config_getter, "get_respect_shebang", return_value=content)
    mocker.patch.object(fixture_config_manager._config_getter, "get_save_all_files_before_run", return_value=content)
    mocker.patch.object(fixture_config_manager._config_getter, "get_save_file_before_run", return_value=content)

    for bool_func in (
        fixture_config_manager.get_ignore_selection,
        fixture_config_manager.get_respect_shebang,
        fixture_config_manager.get_save_all_files_before_run,
        fixture_config_manager.get_save_file_before_run,
    ):
        with expectation:
            result = bool_func()
        if expected is not None:
            assert result == expected
