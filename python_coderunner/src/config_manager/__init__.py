from .basic import (
    IConfigGetter,
    TBasicConfigManager,
    UndefinedValueError,
)
from .config_field import TConfigField
from .exceptions import ConfigFieldNotFoundError, ConfigFieldValidationError
from .interface import IConfig
from .vim_config_manager import TVimConfigGetter, TVimConfigManager

# Public exports
ConfigField = TConfigField
IConfigManager = IConfig  # Backward compatibility alias
