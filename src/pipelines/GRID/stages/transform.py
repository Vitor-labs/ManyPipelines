"""
This module defines the basic flow of data Tranformation from data
retrived from NHTSA.
"""

import logging
from typing import Dict

import httpx
import pandas as pd

from src.utils.logger import setup_logger
from src.utils.decorators import retry, time_logger
from src.utils.funtions import load_categories, load_classifier_credentials

from src.errors.transform_error import TransformError
from src.pipelines.GRID.contracts.extract_contract import ExtractContract
from src.pipelines.GRID.contracts.transform_contract import TransformContract


class DataTransformer:
    """
    Class to define the flow of the data transformation step.

    methods:
        transform -> TransformContract: increase the dataset, adding columns
    """

    logger = logging.getLogger(__name__)
    setup_logger()

    def __init__(self) -> None:
        self.names = []

    @time_logger(logger=logger)
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
        try:
            self.logger.info("Running Transform stage")
            return TransformContract(content=self.__process_new_issue(contract))
        except TransformError as exc:
            raise exc

    def __process_new_issue(self, contract: ExtractContract) -> pd.DataFrame:
        """
        Processes extracted dataset, add new column binning, translate column
        Afected Vehicles to common vehicle. TODO: translate vehicle

        Args:
            contract (ExtractContract): dataset extracted from grid sheet.

        Returns:
            pd.DataFrame: dataframe transformed
        """
        if len(contract.raw_data) == 0:
            raise TransformError("No new data to Classify")

        credentials = load_classifier_credentials()
        issues = pd.DataFrame(contract.raw_data)
        issues["Extracted Date"] = contract.extract_date
        issues["Binning"] = issues.apply(
            lambda row: self.__classify_case(
                row["Issue Title"] + "," + row["Description"], credentials
            ),
            axis=1,
        )
        return issues

    @retry([Exception])
    def __classify_case(self, data: str, credentials: Dict[str, str]) -> str:
        """
        Uses ChatGPT-4.0 to classify each recall by failure mode

        Args:
            data (str): issue title and description
            credentials (Dict[str, str]): api endpoint and authorization token

        Raises:
            exc: ConnectionError, API not responded

        Returns:
            str: result of classificaiton (failure mode)
        """
        text = (
            f"{data}. For this sentences that, check if it is related to onl"
            + f"y one of the following categories: {list(load_categories())}"
            + ". Your answer must be only one of these categories. Note: 'OW"
            + "D' means 'opened while driving' and 'F&F' means 'fit and fini"
            + "sh', for problems related to flushness and margin. Note 2: Fo"
            + "r model Escape (2020 forward), there is a common problem rela"
            + "ted to door check arm when the complaint is related to the do"
            + "or making popping sounds, opening and closing problens, hinge"
            + "s and welds. If you cannot assist, answer NA. You should be o"
            + "bjective and cold. Never change the answer format mentioned a"
            + "nd Never create a new categorie."
        )
        content = {
            "model": "gpt-4",
            "context": (
                "You are a helpful text reader and analyzer. You need to give me 2 answers."
            ),  # sets the overall behavior of the assistant.
            "messages": [{"role": "user", "content": text}],
            "parameters": {
                "temperature": 0.05,  # Determines the randomnes of the model's response.
            },
        }
        try:
            response = httpx.post(
                credentials["url"],
                headers={"Authorization": f"Bearer {credentials['token']}"},
                json=content,
                timeout=360,
            )
        except Exception as exc:
            self.logger.exception(exc)
            self.logger.error(exc)
            raise TransformError(str(exc)) from Exception

        self.logger.info("New response: %s", response.status_code)
        if response.status_code == 200:
            message = response.json()["content"]
            if "\n" in message:
                return message.split("\n")[0]

            return message
        return "NOT CLASSIFIED"
