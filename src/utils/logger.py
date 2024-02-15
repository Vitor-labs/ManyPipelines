"""
This module definies a Logger config for debuging each step of each ETL
pipeline
"""
import json
import logging.config
import pathlib


def setup_logger() -> None:
    """
    Loads configs into logger
    """
    conf_file = pathlib.Path("src/stages/utils/config.json")
    with open(conf_file, "r", encoding="utf-8") as file:
        config = json.load(file)

    logging.config.dictConfig(config)
