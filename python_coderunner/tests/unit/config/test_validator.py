from contextlib import nullcontext as does_not_raise
from typing import Any, ContextManager

import pytest

from src.config import EDispatchersTypes
from src.config.validator import (
    TBoolValidator,
    TDispatchersOrderValidator,
    TDispatchersValidator,
    TStrValidator,
    ValidationError,
)


class TestBoolValidator:
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
        content: Any,
        expected: Any,
        expectation: ContextManager[Any],
    ) -> None:
        validator = TBoolValidator()
        with expectation:
            result = validator.validate(content)
            if expected is not None:
                assert result == expected


class TestStrValidator:
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
        content: Any,
        expected: Any,
        expectation: ContextManager[Any],
    ) -> None:
        """Test string validation with various inputs."""
        validator = TStrValidator()
        with expectation:
            result = validator.validate(content)
            if expected is not None:
                assert result == expected


class TestDispatchersValidator:
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
        content: Any,
        expected: Any,
        expectation: ContextManager[Any],
    ) -> None:
        validator = TDispatchersValidator()
        with expectation:
            result = validator.validate(content)
            if expected is not None:
                assert result == expected


class TestDispatchersOrderValidator:
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
        content: Any,
        expected: Any,
        expectation: ContextManager[Any],
    ) -> None:
        validator = TDispatchersOrderValidator()
        with expectation:
            result = validator.validate(content)
            if expected is not None:
                assert result == expected
