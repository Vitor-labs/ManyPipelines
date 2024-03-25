"""
This module defines the basic flow of data Extraction from NHTSA portal
"""

import os
import re
import logging
from datetime import date, timedelta

import pandas as pd

from src.utils.logger import setup_logger
from src.utils.funtions import create_client
from src.errors.extract_error import ExtractError
from src.utils.decorators import retry, time_logger
from src.contracts.extract_contract import ExtractContract


class DataExtractor:
    """
    Class to define the flow of the data extraction step
    """

    logger = logging.getLogger(__name__)
    setup_logger()

    def __init__(self) -> None:
        """
        TODO: Change to dinamically get the columns from extract schema
        like on NHTSA VOQs pipeline
        """
        self.columns = [
            "REPORT_RECEIVED_DATE",
            "NHTSA_ID",
            "RECALL_LINK",
            "MANUFACTURER",
            "SUBJECT",
            "COMPONENT",
            "MFR_CAMPAIGN_NUMBER",
            "RECALL_TYPE",
            "POTENTIALLY_AFFECTED",
            "RECALL_DESCRIPTION",
            "CONSEQUENCE_SUMMARY",
            "CORRECTIVE_ACTION",
            "PARK_OUTSIDE_ADVISORY",
            "DO_NOT_DRIVE_ADVISORY",
            "COMPLETION_RATE",
        ]

    @time_logger(logger=logger)
    @retry([ConnectionError])
    def extract(self) -> ExtractContract:
        """
        Main method of extraction recalls data from NHTSA

        Raises:
            ExtractError: error occurred during extraction

        Returns:
            ExtractContract: data extracted
        """
        try:
            tomorow = date.today() + timedelta(days=1)
            with create_client() as client:
                response = client.get(
                    "",
                    params={
                        "query": (
                            f"select * where `report_received_date` >= '{os.getenv('LAST_RECALL_WAVE_DATE')}'"
                            + f" AND `report_received_date` < '{date.today().strftime('%Y-%m-%d')}'"
                        ),
                        "read_from_nbe": True,
                        "version": 2.1,
                        "date": tomorow.strftime("%Y-%m-%d"),
                        "accessType": "DOWNLOAD",
                    },
                )
            self.logger.debug("Last updates from %s", response.headers["Last-Modified"])
            return ExtractContract(
                raw_data=self.__process_response(response.text),
                extract_date=date.today(),
            )
        except Exception as exc:
            raise ExtractError(str(exc)) from exc

    def __process_response(self, text: str) -> pd.DataFrame:
        dataset = []
        rows = text.split("\n")
        pattern = r',(?=(?:[^"]*"[^"]*")*[^"]*$)'

        for i in range(1, len(rows)):
            values = re.split(pattern, rows[i])
            if len(values) <= 1:
                break  # the last row always come empty
            dataset.append(values)

        return pd.DataFrame(dataset, columns=self.columns)
