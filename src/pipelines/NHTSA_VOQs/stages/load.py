"""
This module defines the basic flow of data Loading from NHTSA portal
"""

import logging
from typing import cast
from datetime import date

import dotenv
import pandas as pd
from openpyxl import Workbook, load_workbook
from openpyxl.worksheet.worksheet import Worksheet
from src.utils.decorators import time_logger

from src.utils.logger import setup_logger
from src.errors.load_error import LoadError
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
            dotenv.set_key(
                dotenv.find_dotenv(),
                "LAST_COMPLAINT_WAVE_DATE",
                date.today().strftime("%Y%m%d"),
            )
        except Exception as exc:
            raise LoadError(str(exc)) from exc

    def __save_processed_data_csv(self, content: pd.DataFrame) -> None:
        try:
            today = date.today().strftime("%Y-%m-%d")
            path = f"./data/processed/NHTSA_COMPLAINTS_PROCESSED_{today}.csv"

            if content.shape[0] == 0:
                print("There is no new data")
                return

            content.to_csv(path, index=False)

        except Exception as exc:
            raise LoadError(str(exc)) from exc

    def __append_processed_data_excel(self, data: list) -> None:
        path = "./data/raw/F8_BACKUP.xlsx"  # <input the file in this directory>
        sheet_name = "backup"  # <here goes the sheet name>

        if len(data) == 0:
            self.logger.warning("There is no new data")
            return

        try:
            workbook = load_workbook(path)
            sheet = (
                workbook[sheet_name]
                if sheet_name in workbook.sheetnames
                else workbook.create_sheet(sheet_name)
            )
        except FileNotFoundError:  # If the sheet is empty
            workbook = Workbook()
            sheet = cast(Worksheet, workbook.active)
            sheet.title = sheet_name

            # add the header
            for col, key in enumerate(data[0].keys(), start=1):
                cell = sheet.cell(row=1, column=col)
                cell.value = key

        next_row = sheet.max_row + 1 if sheet.max_row > 1 else 1

        # Append the dictionary to the worksheet row by row
        for nrow, rows in enumerate(data, start=0):
            for coln, (_, value) in enumerate(rows.items(), start=1):
                cell = sheet.cell(row=next_row + nrow, column=coln)
                cell.value = value

        workbook.save(path)
