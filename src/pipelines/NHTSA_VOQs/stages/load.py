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
            self.__append_processed_data_excel(contract.content)
            dotenv.set_key(
                dotenv.find_dotenv(),
                "LAST_COMPLAINT_WAVE_DATE",
                date.today().strftime("%Y%m%d"),
            )
        except Exception as exc:
            raise LoadError(str(exc)) from exc

    def __save_processed_data_csv(self, content: pd.DataFrame) -> None:
        today = date.today().strftime("%Y-%m-%d")
        path = f"./data/processed/NHTSA_COMPLAINTS_PROCESSED_{today}.csv"

        if content.shape[0] == 0:
            print("There is no new data")
            raise LoadError("There is no new data")
        try:
            data = content[
                (content["FUNCTION_"] == "F8")
                & (content["MFR_NAME"] != "Ford Motor Company")
            ]
            data.to_csv(path, index=False)
        except Exception as exc:
            raise LoadError(str(exc)) from exc

    def __append_processed_data_excel(self, dataset: pd.DataFrame) -> None:
        path = "./data/raw/F8_BACKUP.xlsx"  # <input the file in this directory>
        sheet_name = "backup"  # <here goes the sheet name>

        if dataset.shape[0] == 0:
            self.logger.warning("There is no new data")
            raise LoadError("There is no new data")
        try:
            data = dataset[dataset["FUNCTION_"] == "F8"]
            with pd.ExcelWriter(path, engine="openpyxl", mode="a") as writer:
                data.to_excel(writer, sheet_name=sheet_name, index=False, header=False)

        except FileNotFoundError as exc:
            raise LoadError(str(exc)) from exc
