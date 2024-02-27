"""
This module defines the basic flow of data Loading from NHTSA portal
"""

import logging
from datetime import date

import dotenv
import pandas as pd

from src.utils.logger import setup_logger
from src.errors.load_error import LoadError
from src.utils.decorators import time_logger
from src.pipelines.NHTSA_VOQs.contracts.transform_contract import TransformContract


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
        self.columsn = []

    @time_logger(logger=logger)
    def load_data(self, contract: TransformContract) -> None:
        """
        Saves data localy in data/processed directory

        Args:
            transform_contract (TransformContract): content processed
        Raises:
            LoadError: Error during serialization.
        """
        try:
            # self.__append_processed_data_excel(contract.content)
            self.__save_other_processed_data_csv(contract.content)
            dotenv.set_key(
                dotenv.find_dotenv(),
                "LAST_RECALL_WAVE_DATE",
                date.today().strftime("%Y%m%d"),
            )
        except Exception as exc:
            self.logger.exception(exc)
            raise LoadError(str(exc)) from exc

    def __save_other_processed_data_csv(self, content: pd.DataFrame) -> None:
        today = date.today().strftime("%Y-%m-%d")
        path = f"./data/processed/NHTSA_RECALLS_PROCESSED_{today}.csv"

        if content.shape[0] == 0:
            print("There is no new data")
            raise LoadError("There is no new data")

        content.to_csv(path, index=False)
