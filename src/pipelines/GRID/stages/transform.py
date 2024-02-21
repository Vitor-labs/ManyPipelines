"""
This module defines the basic flow of data Tranformation from data
retrived from NHTSA.
"""

import os
import time
import logging
from typing import Dict, List
from functools import lru_cache


from src.utils.logger import setup_logger
from src.errors.transform_error import TransformError
from src.pipelines.GRID.contracts.extract_contract import ExtractContract
from src.pipelines.GRID.contracts.transform_contract import TransformContract


class DataTransformer:
    """
    Class to define the flow of the data transformation step.
    TODO: get real car model
    TODO: binning

    methods:
        transform -> TransformContract: increase the dataset, adding columns
    """

    def __init__(self) -> None:
        self.logger = logging.getLogger(__name__)
        setup_logger()

    def transform(self, contract: ExtractContract) -> TransformContract:
        """
        Main flow to tranform data colleted from previews steps

        Args:
            contract (ExtractContract): contract with raw data to transform

        Raises:
            TransformError: Error occouring during this flow

        Returns:
            TransformContract: contract with transformed data to the next step
        """
        start_time = time.time()
        self.logger.info("Running Transform stage")

        try:
            return TransformContract(
                content=self.__process_new_issue(contract.raw_data)
            )
        except TransformError as exc:
            self.logger.exception(exc)
            raise exc
        finally:
            self.logger.info("--- %s minutes ---", round(time.time() - start_time, 2))

    def __process_new_issue(
        self, new_issues: List[Dict[str, str]]
    ) -> List[Dict[str, str]]:
        if len(new_issues) == 0:
            print("No new data to Classify")
            return []
        
        for issue in new_issues:



                
