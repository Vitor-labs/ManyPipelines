"""
This module defines the main flow of processing data.
"""

import time
import logging

from src.utils.logger import setup_logger
from src.pipelines.GRID.stages.load import DataLoader
from src.pipelines.GRID.stages.extract import DataExtractor
from src.pipelines.GRID.stages.transform import DataTransformer


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
        self.logger.debug("Starting: GRID pipeline")
        self.loader.load_data(self.transformer.transform(self.extractor.extract()))
        self.logger.debug(
            "GRID pipeline: completed successfully in %s minutes",
            round((time.time() - start_time) / 60, 2),
        )
