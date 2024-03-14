"""
This module defines the basic flow of data Loading from NHTSA portal
"""

import logging
from datetime import date
from sqlite3 import OperationalError

import pandas as pd
from dotenv import set_key, find_dotenv

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
        self.path = f"./data/processed/NHTSA_COMPLAINTS_PROCESSED_{self.today}.csv"

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
            # self.__update_env_vars(contract.content["ODINO"].max())
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
            # TODO: load to sqlite, change to cloud SQL
            content.to_sql(
                "Complaints", DBConnector.local, if_exists="append", index=False
            )
        except OperationalError as exc:
            raise exc
        self.logger.info("Database uploaded with run of %s", self.today)

    def __update_env_vars(self, odino: int) -> None:
        set_key(
            find_dotenv(),
            "LAST_COMPLAINT_WAVE_DATE",
            date.today().strftime("%Y%m%d"),
        )
        set_key(
            find_dotenv(),
            "LAST_ODINO_CAPTURED",
            str(odino),
        )
