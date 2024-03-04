"""
This module definies a Logger config for debuging each step of each ETL
pipeline
"""

import json
import logging.config


def setup_logger() -> None:
    """
    Loads configs into logger
    TODO: add color to logs - https://pypi.org/project/coloredlogs/
    """
    with open("./src/utils/config.json", "r", encoding="utf-8") as file:
        config = json.load(file)

    logging.config.dictConfig(config)
