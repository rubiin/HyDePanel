import json
import os

import pytomlpp
from fabric.utils import get_relative_path
from loguru import logger

from .constants import DEFAULT_CONFIG
from .functions import exclude_keys, flatten_dict, merge_defaults, validate_widgets
from .widget_settings import BarConfig


class HydeConfig:
    "A class to read the configuration file and return the default configuration"

    instance = None

    @staticmethod
    def get_default():
        if HydeConfig.instance is None:
            HydeConfig.instance = HydeConfig()

        return HydeConfig.instance

    def __init__(self):
        self.json_config = get_relative_path("../config.json")
        self.toml_config = get_relative_path("../config.toml")
        self.default_config()
        self.parse_styles()

    # Function to read the configuration file in json
    def read_config_json(self) -> dict:
        logger.info(f"[Config] Reading json config from {self.json_config}")
        with open(self.json_config) as file:
            # Load JSON data into a Python dictionary
            data = json.load(file)
        return data

    # Function to read the configuration file in json
    def read_config_toml(self) -> dict:
        logger.info(f"[Config] Reading toml config from {self.toml_config}")
        with open(self.toml_config) as file:
            # Load JSON data into a Python dictionary
            data = pytomlpp.load(file)
        return data

    def default_config(self) -> BarConfig:
        # Read the configuration from the JSON file
        check_toml = os.path.exists(self.toml_config)
        check_json = os.path.exists(self.json_config)

        if not check_json and not check_toml:
            raise FileNotFoundError("Please provide either a json or toml config.")

        parsed_data = self.read_config_json() if check_json else self.read_config_toml()

        validate_widgets(parsed_data, DEFAULT_CONFIG)

        for key in exclude_keys(DEFAULT_CONFIG, ["$schema"]):
            if key == "module_groups":
                # For lists, use the user's value or default if not present
                parsed_data[key] = parsed_data.get(key, DEFAULT_CONFIG[key])
            else:
                # For dictionaries, merge with defaults
                parsed_data[key] = merge_defaults(
                    parsed_data.get(key, {}), DEFAULT_CONFIG[key]
                )

        self.config = parsed_data

    def parse_styles(self):
        theme = flatten_dict(self.config["theme"])

        return {
            "font-size": lambda: f"font-size: {theme['font-size']};",
            "font-family": lambda: f"font-family: {theme['font-family']};",
            "font-weight": lambda: f"font-weight: {theme['font-weight']};",
        }


widget_config = HydeConfig().get_default().config
widget_styles = HydeConfig().get_default().parse_styles()
