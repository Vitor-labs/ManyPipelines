"""
This module defines the basic flow of data Loading from NHTSA portal
"""

import logging
from datetime import date
from sqlite3 import OperationalError

import pandas as pd

from src.utils.logger import setup_logger
from src.errors.load_error import LoadError
from src.utils.decorators import time_logger
from src.infra.db_connection import DBConnector
from src.contracts.transform_contract import TransformContract


class DataLoader:
    """
    Class to define the flow of saving the data already transformed into CSV's
    and GCP Cloud SQL.

    methods:
        load_data: saves processed data in serialized file and database.
    """

    logger = logging.getLogger(__name__)
    setup_logger()

    def __init__(self) -> None:
        self.today = date.today().strftime("%Y-%m-%d")
        self.path = f"./data/processed/VIN_INFO_{self.today}.csv"

    @time_logger(logger=logger)
    def load_data(self, contract: TransformContract) -> None:
        """
        Saves data localy in data/processed directory

        Args:
            transform_contract (TransformContract): content processed
        Raises:.
            LoadError: Error during serialization.
        """
        if contract.content.shape[0] == 0:
            raise LoadError("There is no new data")
        try:
            self.__save_other_processed_data_csv(contract.content)
            self.__load_on_database(contract.content)
        except Exception as exc:
            self.logger.exception(exc)
            raise LoadError(str(exc)) from exc

    def __save_other_processed_data_csv(self, content: pd.DataFrame) -> None:
        content.to_csv(self.path, index=False)
        self.logger.info(
            "Run of (%s) done. Weekly data saved on %s", self.today, self.path
        )

    def __load_on_database(self, content: pd.DataFrame) -> None:
        try:
            content.to_sql(
                "Dim_VinInfo", DBConnector.local, if_exists="append", index=False
            )
        except OperationalError as exc:
            raise exc

        self.logger.info("Database uploaded with run of %s", self.today)
