"""
This module defines the basic flow of data Loading from NHTSA portal
"""

import logging
from datetime import date
from typing import NoReturn

import dotenv
import pandas as pd
from openpyxl import load_workbook, Workbook

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
        if contract.content.shape[0] == 0:
            print("There is no new data")
            raise LoadError("There is no new data")
        try:
            self.__append_processed_data_excel(contract.content)
            self.__save_other_processed_data_csv(contract.content)
            self.__update_env_vars(contract.content["ODINO"].max())
        except Exception as exc:
            self.logger.exception(exc)
            raise LoadError(str(exc)) from exc

    def __save_other_processed_data_csv(self, content: pd.DataFrame) -> None:
        today = date.today().strftime("%Y-%m-%d")
        path = f"./data/processed/NHTSA_COMPLAINTS_PROCESSED_{today}.csv"

        content.to_csv(path, index=False)

    def __update_env_vars(self, odino: str) -> None:
        dotenv.set_key(
            dotenv.find_dotenv(),
            "LAST_COMPLAINT_WAVE_DATE",
            date.today().strftime("%Y%m%d"),
        )
        dotenv.set_key(
            dotenv.find_dotenv(),
            "LAST_ODINO_CAPTURED",
            odino,
        )

    def __append_processed_data_excel(self, dataset: pd.DataFrame) -> None:
        path = "./data/raw/F8_BACKUP.xlsx"  # <input the file in this directory>
        sheet_name = "backup"  # <here goes the sheet name>
        # TODO: parse formulas on certain columns https://openpyxl.readthedocs.io/en/stable/formula.html
        try:
            data = dataset[dataset["FUNCTION_"] == "F8"]
            with pd.ExcelWriter(  # pylint: disable=abstract-class-instantiated
                path, engine="openpyxl", mode="a", if_sheet_exists="overlay"
            ) as writer:
                data[
                    [
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
                ].to_excel(
                    writer,
                    sheet_name=sheet_name,
                    startrow=writer.sheets[sheet_name].max_row,
                    index=False,
                    header=False,
                )
        except FileNotFoundError as exc:
            self.logger.info(exc)

            workbook = Workbook()
            workbook.create_sheet(sheet_name)
            sheet = workbook.active
            sheet.append(list(data.columns))  # type: ignore

            workbook.save(path)

            self.logger.info("%s Created", path)
            self.__append_processed_data_excel(data)

        except Exception as exc:
            raise LoadError(str(exc)) from exc
