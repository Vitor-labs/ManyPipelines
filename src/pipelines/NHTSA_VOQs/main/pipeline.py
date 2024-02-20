"""
This module defines the main flow of processing data.
"""

import time
import logging

from src.utils.logger import setup_logger
from src.pipelines.NHTSA_VOQs.stages.load import DataLoader
from src.pipelines.NHTSA_VOQs.stages.extract import DataExtractor
from src.pipelines.NHTSA_VOQs.stages.transform import DataTransformer


class Pipeline:
    """
    Class to define the main flow of data processing
    """

    def __init__(self) -> None:
        self.logger = logging.getLogger(__name__)
        self.extractor = DataExtractor()
        self.transformer = DataTransformer()
        self.loader = DataLoader()
        setup_logger()

    def run(self) -> None:
        """
        Main flow of data processing
        """
        start_time = time.time()
        self.logger.debug("Starting the ETL pipeline")
        extracted = self.extractor.extract()
        transformed = self.transformer.transform(extracted)
        self.loader.load_data(transformed)
        self.logger.debug("ETL pipeline completed successfully")
        self.logger.debug(
            "--- %s minutes ---", round((time.time() - start_time) / 60, 2)
        )
