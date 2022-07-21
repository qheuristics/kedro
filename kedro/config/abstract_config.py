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
        **kwargs
    ):
        super().__init__()
        self.conf_source = conf_source
        self.env = env
        self.runtime_params = runtime_params

        self.mapping = kwargs

    def __getitem__(self, key):
        # TODO: Discuss: I think I remember we decided to hard-code what's commented out below,
        #  but then users still wouldn't be able to provide custom entries for any of the
        #  "mandatory" configs, so I feel like we should just return the pattern from the dict?

        # if key == "catalog":
        #     return self.get("catalog*", "catalog*/**", "**/catalog*")
        # if key == "parameters":
        #     return self.get("parameters*", "parameters*/**", "**/parameters*")
        # if key == "credentials":
        #     return self.get("credentials*", "credentials*/**", "**/credentials*")
        # if key == "logging":
        #     return self.get("logging*", "logging*/**", "**/logging*")
        patterns = self.mapping[key]
        return self.get(patterns)

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
