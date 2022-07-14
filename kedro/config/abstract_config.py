"""This module provides ``kedro.abstract_config`` with the baseline
class model for a `ConfigLoader` implementation.
"""
from abc import ABC, abstractmethod
from collections.abc import MutableMapping
from typing import Any, Dict


class AbstractConfigLoader(MutableMapping):
    """``AbstractConfigLoader`` is the abstract base class
        for all `ConfigLoader` implementations.
    All user-defined `ConfigLoader` implementations should inherit
        from `AbstractConfigLoader` and implement all relevant abstract methods.
    """

    def __init__(
        self,
        catalog,
        parameters,
        credentials,
        logging,
        conf_source: str,
        env: str = None,
        runtime_params: Dict[str, Any] = None,
        **kwargs  # pylint: disable=unused-argument
    ):
        self.conf_source = conf_source
        self.env = env
        self.runtime_params = runtime_params

        self.mapping = {}
        # Mandatory configs
        self.mapping["catalog"] = catalog
        self.mapping["parameters"] = parameters
        self.mapping["credentials"] = credentials
        self.mapping["logging"] = logging

    def __getitem__(self, key):
        return self.mapping[key]

    def __delitem__(self, key):
        value = self[key]
        del self.mapping[key]
        self.pop(value, None)

    def __setitem__(self, key, value):
        if key in self:
            del self[self[key]]
        self.mapping[key] = value

    def __iter__(self):
        return iter(self.mapping)

    def __len__(self):
        return len(self.mapping)

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
