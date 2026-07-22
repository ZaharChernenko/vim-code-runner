from typing import Any

class error(Exception):
    """Upon encountering a Vim error, Python raises an exception of type vim.error."""

    pass

class _Buffer(list[str]):
    """Buffer object representing a vim buffer. Acts as a list of strings."""

    name: str
    number: int
    valid: bool

class _Current:
    """An object providing access to various 'current' objects available in vim."""

    line: str
    buffer: _Buffer
    window: Any
    tabpage: Any
    range: Any

current: _Current

def command(cmd: str) -> None:
    """Executes the vim (ex-mode) command cmd. Returns None."""
    ...

def eval(expr: str) -> Any:
    """
    Evaluates the expression expr using the vim internal expression evaluator.
    Returns the expression result as a string, list, tuple, dictionary, boolean, or None."""
    ...
