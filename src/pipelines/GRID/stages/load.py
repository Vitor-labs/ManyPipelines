"""
This module defines the basic flow of data Loading from NHTSA portal
"""

import logging
from datetime import date
from sqlite3 import OperationalError

import dotenv
import pandas as pd

from src.utils.logger import setup_logger
from src.errors.load_error import LoadError
from src.utils.decorators import time_logger
from src.infra.db_connection import DBConnector
from src.contracts.transform_contract import TransformContract


class DataLoader:
    """
    Class to define the flow of saving the data already transformed into CSV
    and GCP Cloud SQL.

    methods:
        load_data: saves processed data in serialized file and database.
    """

    logger = logging.getLogger(__name__)
    setup_logger()

    def __init__(self) -> None:
        self.today = date.today().strftime("%Y-%m-%d")
        self.path = f"./data/processed/NHTSA_COMPLAINTS_PROCESSED_{self.today}.csv"

    @time_logger(logger)
    def load_data(self, contract: TransformContract) -> None:
        """
        Saves data localy in data/processed directory

        Args:
            transform_contract (TransformContract): content processed

        Raises:
            LoadError: Error during serialization.
        """
        try:
            self.logger.info("Running Load stage")
            self.__save_processed_data_csv(contract.content)
            self.__load_on_database(contract.content)
            self.__update_env_vars(contract.content["Issue #"].max())
        except Exception as exc:
            raise LoadError(str(exc)) from exc

    def __save_processed_data_csv(self, content: pd.DataFrame) -> None:
        try:
            content.to_csv(self.path, index=False)

        except Exception as exc:
            raise LoadError(str(exc)) from exc

    def __load_on_database(self, content: pd.DataFrame) -> None:
        try:
            content.to_sql(
                "Dim_GRID", DBConnector.local, if_exists="append", index=False
            )
        except OperationalError as exc:
            raise exc
        self.logger.info("Database uploaded with run of %s", self.today)

    def __update_env_vars(self, last_grid_issue) -> None:
        dotenv.set_key(
            dotenv.find_dotenv(),
            "LAST_GRID_ISSUE_DATE",
            date.today().strftime("%Y-%m-%d"),
        )
        dotenv.set_key(
            dotenv.find_dotenv(),
            "GRID_LAST_ISSUE",
            last_grid_issue,
        )
