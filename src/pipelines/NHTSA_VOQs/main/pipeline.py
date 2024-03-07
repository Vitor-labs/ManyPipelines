"""
This module defines the main flow of processing data.
"""

import logging
from src.utils.decorators import time_logger

from src.utils.logger import setup_logger
from src.pipelines.NHTSA_VOQs.stages.load import DataLoader
from src.pipelines.NHTSA_VOQs.stages.extract import DataExtractor
from src.pipelines.NHTSA_VOQs.stages.transform import DataTransformer


class Pipeline:
    """
    Class to define the main flow of data processing
    """

    logger = logging.getLogger(__name__)
    setup_logger()

    def __init__(self) -> None:
        self.extractor = DataExtractor()
        self.transformer = DataTransformer()
        self.loader = DataLoader()

    @time_logger(logger=logger)
    async def run(self) -> None:
        """
        Main flow of data processing
        """
        self.logger.info("Starting the ETL pipeline")
        self.loader.load_data(
            await self.transformer.transform(self.extractor.extract())
        )
        self.logger.info("ETL pipeline completed successfully")
