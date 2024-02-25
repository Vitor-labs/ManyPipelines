"""
This module defines the basic flow of data Loading from NHTSA portal
"""

import time
import logging
from datetime import date

import dotenv
import pandas as pd
from src.utils.decorators import time_logger

from src.utils.logger import setup_logger
from src.errors.load_error import LoadError
from src.pipelines.GRID.contracts.transform_contract import TransformContract


class DataLoader:
    """
    Class to define the flow of saving the data already transformed into CSV
    and GCP Cloud SQL.

    methods:
        load_data: saves processed data in serialized file and database.
    """

    def __init__(self) -> None:
        self.logger = logging.getLogger(__name__)
        setup_logger()

    @time_logger
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
            dotenv.set_key(
                dotenv.find_dotenv(),
                "LAST_GRID_ISSUE_DATE",
                date.today().strftime("%Y-%m-%d"),
            )
        except Exception as exc:
            raise LoadError(str(exc)) from exc

    def __save_processed_data_csv(self, content: pd.DataFrame) -> None:
        try:
            today = date.today().strftime("%Y-%m-%d")
            path = f"./data/processed/GRID_PROCESSED_{today}.csv"

            if content.shape[0] == 0:
                print("There is no new data")
                return

            content.to_csv(path, index=False)

        except Exception as exc:
            raise LoadError(str(exc)) from exc
