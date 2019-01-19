"""Configuration Module."""
from pathlib import Path
from typing import Optional, Dict

import yaml

from src.common.environment import Environment
from src.infractuture.configuration.missing_section_error import MissingSectionError


class Configuration:
    """Read configuration from file."""

    _USER_CONFIG_PATH = "configuration.yaml"
    _DEFAULT_CONFIG_PATH = "configuration-default.yaml"
    _GENERAL_SECTION = 'general'

    def __init__(
            self,
            *,
            environment: Environment = None,
            user_config_path: Optional[Path] = None,
            default_config_path: Optional[Path] = None) -> None:
        """Get a configuration object with a configuration file read.
        :param user_config_path: optionally override the file to be read.
        """
        self.user_config_path = user_config_path or self._USER_CONFIG_PATH
        try:
            with open(self.user_config_path, 'r') as f:
                user_config = yaml.load(f, Loader=yaml.SafeLoader)
        except FileNotFoundError:
            # TODO: LOG IN DEBUG MODE
            user_config = {}

        default_config_path = default_config_path or self._DEFAULT_CONFIG_PATH
        with open(default_config_path, 'r') as f:
            default_config = yaml.load(f, Loader=yaml.SafeLoader)

        environment = self._get_environment(
            force_environment=environment,
            default_config=default_config,
            user_config=user_config)

        self._config = self._merge_user_and_default_config(environment=environment, default_config=default_config, user_config=user_config)

    def get_section(self, *, section: str) -> Dict[str, str]:
        """Get a configuration section.
        :param section: (str) The configuration section.
        :return: (dict) dictionary of values).
        """
        try:
            return self._config[section]
        except KeyError:
            raise MissingSectionError(f"Missing section '{section}'")

    def save_user_file(self, *, data: Dict) -> None:
        """Save user configuration in a file

        :param data: (dict) The configuration data to save in a yaml file.
        :return: None
        """
        with open(self.user_config_path, 'w') as user_config_file:
            yaml.dump(data, user_config_file)

    def _merge_user_and_default_config(self, *, environment: Environment, default_config: dict, user_config: dict) -> dict:
        config = {}

        sections = list(default_config.keys()) + list(user_config.keys())
        sections.remove(self._GENERAL_SECTION)

        for section in sections:
            try:
                user_section_config = user_config[section][environment.value]
            except KeyError:
                user_section_config = {}
            try:
                default_section_config = default_config[section][environment.value]
            except KeyError:
                default_section_config = {}

            config[section] = {**default_section_config, **user_section_config}

        return config

    def _get_environment(
            self,
            *,
            force_environment: Environment,
            default_config: dict,
            user_config: dict) -> Environment:
        if force_environment:
            return Environment(force_environment)

        try:
            user = user_config[self._GENERAL_SECTION]['environment']
        except KeyError:
            user = None

        if user:
            return Environment(user)

        return Environment(default_config[self._GENERAL_SECTION]['environment'])
