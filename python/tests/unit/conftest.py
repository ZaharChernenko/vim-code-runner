import sys
from unittest.mock import MagicMock


def pytest_configure():
    sys.modules["vim"] = MagicMock()
