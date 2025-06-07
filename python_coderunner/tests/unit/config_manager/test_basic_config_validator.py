from contextlib import nullcontext as does_not_raise

import pytest

from src.config_manager import EDispatchersTypes, TBasicConfigValidator, ValidationError


class TestConfigValidator:
    @pytest.mark.parametrize(
        ("content", "expected", "expectation"),
        (
            (True, True, does_not_raise()),
            (False, False, does_not_raise()),
            ("1", True, does_not_raise()),
            ("0", False, does_not_raise()),
            (1, True, does_not_raise()),
            (0, False, does_not_raise()),
            ("invalid", None, pytest.raises(ValidationError)),
            (None, None, pytest.raises(ValidationError)),
        ),
    )
    def test_validate_bool(
        self,
        fixture_config_validator: TBasicConfigValidator,
        content,
        expected,
        expectation,
    ):
        with expectation:
            result = fixture_config_validator.validate_bool(content)
        if expected is not None:
            assert result == expected

    @pytest.mark.parametrize(
        ("content", "expected", "expectation"),
        (
            ("test string", "test string", does_not_raise()),
            ("", "", does_not_raise()),
            ("123", "123", does_not_raise()),
            (123, None, pytest.raises(ValidationError)),
            (True, None, pytest.raises(ValidationError)),
            (None, None, pytest.raises(ValidationError)),
            ([], None, pytest.raises(ValidationError)),
            ({}, None, pytest.raises(ValidationError)),
        ),
    )
    def test_validate_str(
        self,
        fixture_config_validator: TBasicConfigValidator,
        content,
        expected,
        expectation,
    ):
        with expectation:
            result = fixture_config_validator.validate_str(content)
            if expected is not None:
                assert result == expected

    @pytest.mark.parametrize(
        ("content", "expected", "expectation"),
        (
            (
                {"*.py": "python", "*.js": "node"},
                {"*.py": "python", "*.js": "node"},
                does_not_raise(),
            ),
            ({"*.py": "python"}, {"*.py": "python"}, does_not_raise()),
            ("invalid", None, pytest.raises(ValidationError)),
            (123, None, pytest.raises(ValidationError)),
            (None, None, pytest.raises(ValidationError)),
            ({"*.py": 123}, None, pytest.raises(ValidationError)),
            ({123: "python"}, None, pytest.raises(ValidationError)),
        ),
    )
    def test_validate_dispatcher(
        self,
        fixture_config_validator: TBasicConfigValidator,
        content,
        expected,
        expectation,
    ):
        with expectation:
            result = fixture_config_validator.validate_dispatcher(content)
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
            (["invalid"], None, pytest.raises(ValidationError)),
            ([1], None, pytest.raises(ValidationError)),
            ({}, None, pytest.raises(ValidationError)),
        ),
    )
    def test_validate_dispatchers_order(
        self,
        fixture_config_validator: TBasicConfigValidator,
        content,
        expected,
        expectation,
    ):
        with expectation:
            result: list[EDispatchersTypes] = fixture_config_validator.validate_dispatchers_order(content)
        if expected is not None:
            assert result == expected
