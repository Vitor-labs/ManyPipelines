"""
This module defines the basic flow of data Extraction from NHTSA portal
"""

import logging
from typing import List
from datetime import date

import pandas as pd

from src.utils.logger import setup_logger
from src.contracts.schemas.extract import schema
from src.errors.extract_error import ExtractError
from src.utils.decorators import retry, time_logger
from src.contracts.extract_contract import ExtractContract


class DataExtractor:
    """
    Class to define the flow of the data extraction step.
    """

    logger = logging.getLogger(__name__)
    setup_logger()

    def __init__(self) -> None:
        self.columns: List[str] = list(schema.columns.keys())

    @time_logger(logger)
    @retry([ConnectionError])
    def extract(self) -> ExtractContract:
        """
        Main method of extraction for Vins

        Raises:
            ExtractError: error occurred during extraction

        Returns:
            ExtractContract: data extracted
        """
        try:
            retrived = self.__load_full_vins()
            self.logger.info("Collected %s new cases", retrived.shape[0])

            return ExtractContract(raw_data=retrived, extract_date=date.today())

        except Exception as exc:
            self.logger.exception(exc)
            raise ExtractError(str(exc)) from exc

    def __load_full_vins(self) -> pd.DataFrame:
        """
        Loads newest full vins.
        TODO: modify origin to sharepoint.

        Returns:
            Dict[str, str]: dict with odino as key and full vin as value
        """
        df = pd.read_excel(
            "./data/external/NSCCV-000502-20240304.xlsx", sheet_name="VOQS"
        )
        df.dropna(inplace=True)
        df = df[~df["VIN"].str.endswith("*") & (df["VIN"] != "") & (df["VIN"] != "N/A")]

        return df.set_index("ODI_ID")
