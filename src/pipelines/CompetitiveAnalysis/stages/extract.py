"""
This module defines the basic flow of data Extraction from NHTSA portal
"""

import os
import time
import logging
from datetime import date, timedelta

from src.utils.decorators import retry
from src.utils.logger import setup_logger
from src.utils.funtions import create_client
from src.errors.extract_error import ExtractError
from src.pipelines.NHTSA_VOQs.contracts.extract_contract import ExtractContract


class DataExtractor:
    """
    Class to define the flow of the data extraction step
    """

    def __init__(self) -> None:
        self.logger = logging.getLogger(__name__)
        setup_logger()

    @retry([ConnectionError])
    def extract(self) -> ExtractContract:
        """
        Main method of extraction recalls data from NHTSA

        Raises:
            ExtractError: error occurred during extraction

        Returns:
            ExtractContract: data extracted
        """
        start_time = time.time()
        self.logger.debug("\nRunning Extract stage")
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
                print(response.headers["Last-Modified"])
                data = response.text

                # TODO: process dataset

            return ExtractContract(raw_data=data, extract_date=date.today())

        except Exception as exc:
            raise ExtractError(str(exc)) from exc

        finally:
            self.logger.debug("--- %s seconds ---", round(time.time() - start_time, 2))
