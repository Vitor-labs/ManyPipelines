"""
This module defines the main flow of processing data.
"""

import logging

from src.utils.logger import setup_logger
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
        self.loader = None
        setup_logger()

    def run(self) -> None:
        """
        Main flow of data processing
        """
        self.logger.info("Running main pipeline")
        extracted = self.extractor.extract()
        transformed = self.transformer.transform(extracted)
