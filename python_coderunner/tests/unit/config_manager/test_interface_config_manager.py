from contextlib import nullcontext as does_not_raise

import pytest
import pytest_mock

from src.config_manager import EDispatchersTypes, IConfigManager


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
    fixture_config_manager: IConfigManager,
    content,
    expected,
    expectation,
    mocker: pytest_mock.MockFixture,
):
    mocker.patch.object(fixture_config_manager, "_get_glob_to_command_impl", return_value=content)
    mocker.patch.object(fixture_config_manager, "_get_file_ext_to_command_impl", return_value=content)
    mocker.patch.object(fixture_config_manager, "_get_file_type_to_command_impl", return_value=content)
    with expectation:
        result = fixture_config_manager.get_glob_to_command()
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
    fixture_config_manager: IConfigManager, content, expected, expectation, mocker: pytest_mock.MockFixture
):
    mocker.patch.object(fixture_config_manager, "_get_dispatchers_order_impl", return_value=content)
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
    fixture_config_manager: IConfigManager,
    content,
    expected,
    expectation,
    mocker: pytest_mock.MockFixture,
):
    mocker.patch.object(fixture_config_manager, "_get_ignore_selection_impl", return_value=content)
    mocker.patch.object(fixture_config_manager, "_get_respect_shebang_impl", return_value=content)
    mocker.patch.object(fixture_config_manager, "_get_save_all_files_impl", return_value=content)
    mocker.patch.object(fixture_config_manager, "_get_save_file_impl", return_value=content)

    for bool_func in (
        fixture_config_manager.get_ignore_selection,
        fixture_config_manager.get_respect_shebang,
        fixture_config_manager.get_save_all_files,
        fixture_config_manager.get_save_file,
    ):
        with expectation:
            result = bool_func()
        if expected is not None:
            assert result == expected
