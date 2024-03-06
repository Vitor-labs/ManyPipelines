"""
This module defines the basic flow of data Loading from NHTSA portal
"""

import logging
from datetime import date

import pandas as pd
from openpyxl import Workbook
from dotenv import set_key, find_dotenv

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
        self.columns = [
            "CMPLID",
            "ODINO",
            "MAKETXT",
            "MODELTXT",
            "YEARTXT",
            "FAILDATE",
            "FAIL_QUARTER",
            "DATEA",
            "PROD_DATE",
            "EXTRACTED_DATE",
            "FULL_VIN",
            "VIN",
            "FUNCTION_",
            "CDESCR",
            "BINNING",
            "VFG",
            "COMPONET",
            "FAILURE",
            "CRASH",
            "FIRE",
            "INJURED",
            "DEATHS",
            "MILES",
            "STATE",
            "VEH_SPEED",
            "DEALER_NAME",
            "DEALER_STATE",
            "To_be_Binned",
            "VEHICLE_LINE_WERS",
            "VEHICLE_LINE_GSAR",
            "VEHICLE_LINE_GLOBAL",
            "ASSEMBLY_PLANT",
            "WARRANTY_START_DATE",
            "REPAIR_DATE_1",
            "REPAIR_DATE_2",
            "FAILURE_MODE",
            "NewOld",
            "New_Failure_Mode",
            "MILEAGE_CLASS",
        ]

    @time_logger(logger=logger)
    def load_data(self, contract: TransformContract) -> None:
        """
        Saves data localy in data/processed directory

        Args:
            transform_contract (TransformContract): content processed
        Raises:
            LoadError: Error during serialization.
        """
        if contract.content.shape[0] == 0:
            print("There is no new data")
            raise LoadError("There is no new data")
        try:
            self.__save_other_processed_data_csv(contract.content)
            self.__update_env_vars(contract.content["ODINO"].max())
        except Exception as exc:
            self.logger.exception(exc)
            raise LoadError(str(exc)) from exc

    def __save_other_processed_data_csv(self, content: pd.DataFrame) -> None:
        today = date.today().strftime("%Y-%m-%d")
        path = f"./data/processed/NHTSA_COMPLAINTS_PROCESSED_{today}.csv"

        content.to_csv(path, index=False)
        self.logger.info("Run of (%s) done. Weekly data saved on %s", today, path)

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
