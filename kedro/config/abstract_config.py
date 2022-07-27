"""This module provides ``kedro.abstract_config`` with the baseline
class model for a `ConfigLoader` implementation.
"""
from abc import abstractmethod
from typing import Any, Dict


class AbstractConfigLoader(dict):
    """``AbstractConfigLoader`` is the abstract base class
        for all `ConfigLoader` implementations.
    All user-defined `ConfigLoader` implementations should inherit
        from `AbstractConfigLoader` and implement all relevant abstract methods.
    """

    def __init__(
        self,
        conf_source: str,
        env: str = None,
        runtime_params: Dict[str, Any] = None,
        **kwargs  # pylint: disable=unused-argument
    ):
        super().__init__()
        self.conf_source = conf_source
        self.env = env
        self.runtime_params = runtime_params

    # TODO: Here for backwards compatibility. Needs to be removed in 0.19.0.
    def __getitem__(self, key):
        # pylint: disable=too-many-function-args
        if key == "catalog":
            return self.get("catalog*", "catalog*/**", "**/catalog*")
        if key == "parameters":
            return self.get("parameters*", "parameters*/**", "**/parameters*")
        if key == "credentials":
            return self.get("credentials*", "credentials*/**", "**/credentials*")
        if key == "logging":
            return self.get("logging*", "logging*/**", "**/logging*")
        return super().__getitem__(key)

    @abstractmethod  # pragma: no cover
    def get(self) -> Dict[str, Any]:
        """Required method to get all configurations."""
        pass


class BadConfigException(Exception):
    """Raised when a configuration file cannot be loaded, for instance
    due to wrong syntax or poor formatting.
    """

    pass


class MissingConfigException(Exception):
    """Raised when no configuration files can be found within a config path"""

    pass
