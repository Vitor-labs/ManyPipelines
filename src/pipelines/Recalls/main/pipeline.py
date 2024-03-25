"""
This module defines the main flow of processing data.
"""

import logging
from src.utils.decorators import time_logger

from src.utils.logger import setup_logger
from src.infra.db_connection import DBConnector
from src.pipelines.Recalls.stages.load import DataLoader
from src.pipelines.Recalls.stages.extract import DataExtractor
from src.pipelines.Recalls.stages.transform import DataTransformer


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
    def run(self) -> None:
        """
        Main flow of data processing
        """

        DBConnector.connect_local()
        self.logger.info("Starting the ETL pipeline")
        self.loader.load_data(self.transformer.transform(self.extractor.extract()))
        self.logger.info("ETL pipeline completed successfully")
