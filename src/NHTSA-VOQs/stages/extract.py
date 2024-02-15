"""
This module defines the basic flow of data Extraction from NHTSA portal
"""

import time
import logging
from datetime import date

from src.drives.interfaces.http_request import HttpRequestInterface
from src.drives.interfaces.structure_dataset import (
    StructureDatasetInterface,
)
from src.utils.decorators import retry
from src.utils.logger import setup_logger
from src.errors.extract_error import ExtractError


class DataExtractor:
    """
    Class to define the flow of the data extraction step
    """

    def __init__(
        self, request: HttpRequestInterface, collector: StructureDatasetInterface
    ) -> None:
        self.__request = request
        self.__collector = collector
        self.logger = logging.getLogger(__name__)
        setup_logger()

    @retry([ConnectionError])
    def extract(self):
        """
        Main method of extraction

        Raises:
            ExtractError: error occurred during extraction

        Returns:
            ExtractContract: data extracted
        """
        start_time = time.time()
        self.logger.debug("\nRunning Extract stage")
        try:
            data = self.__request.request_content_from_url()
            retrived = self.__collector.assemble_data(data)
            return ExtractContract(raw_data=retrived, extract_date=date.today())

        except Exception as exc:
            raise ExtractError(str(exc)) from exc

        finally:
            self.logger.debug("--- %s seconds ---", round(time.time() - start_time, 2))
