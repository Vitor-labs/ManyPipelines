"""
This module defines the basic flow of data Tranformation from data
retrived from NHTSA.
"""

import logging
from functools import lru_cache

import httpx
from pandas import to_datetime

from src.utils.logger import setup_logger
from src.errors.transform_error import TransformError
from src.contracts.extract_contract import ExtractContract
from src.contracts.transform_contract import TransformContract
from src.utils.decorators import rate_limiter, retry, time_logger
from src.utils.funtions import (
    extract_url,
    load_categories,
    load_classifier_credentials,
)


class DataTransformer:
    """
    Class to define the flow of the data transformation step

    methods:
        transform -> TransformContract: increase the dataset, adding columns
    """

    logger = logging.getLogger(__name__)
    setup_logger()

    def __init__(self) -> None:
        self.parts = (
            "door, window, windshield, wiper, glass, hood, trunk, moonroof, "
            + "bumper, tail light, pillar, undershield, roof rack, latch, he"
            + "adlight, door handle, door keypad, window, weatherstripping, "
            + "side mirror, lighting, swing gate, cowl grille, hard top, ski"
            + "d plate, sheet metal, running boards, water leak, etc"
        )
        self.credentials = load_classifier_credentials()

    @time_logger(logger=logger)
    def transform(self, contract: ExtractContract) -> TransformContract:
        """
        Main flow to tranform data colleted from previews steps

        Args:
            contract (ExtractContract): contract with raw data to transform
            flag (DatasetFlag): dataset typo

        Raises:
            TransformError: Error occouring during this flow

        Returns:
            TransformContract: contract with transformed data to the next step
        """
        data = contract.raw_data

        try:
            data["REPORT_RECEIVED_DATE"] = to_datetime(
                data["REPORT_RECEIVED_DATE"], format="%Y-%m-%d"
            ).dt.strftime("%m-%d-%Y")
            data["RECALL_LINK"].apply(extract_url)
            data["POTENTIALLY_AFFECTED"] = data["POTENTIALLY_AFFECTED"].astype(int)
            data["PROBLEM_ID"] = data.apply(
                lambda row: self.__classify_case(
                    (
                        f'With this problematic component {str(row["COMPONENT"])} '
                        + f'and this decription: {str(row["RECALL_DESCRIPTION"])}.'
                    )
                )
            )
            data["EXTRACTED_DATE"] = contract.extract_date

            return TransformContract(content=data)
        except TransformError as exc:
            self.logger.exception(exc)
            raise exc

    @retry([Exception])
    @rate_limiter(70, 1)
    @lru_cache(maxsize=70)
    def __classify_case(self, prompt: str) -> str:
        """
        Uses ChatGPT-4.0 to classify each recall by Binning

        Args:
            prompt (str): prompt primary text

        Returns:
            str: result of classificaiton
        """
        text = (
            "Question 1: For this description, check if it's related to an e"
            + f"xternal part of the car, body exterior, ({self.parts}). If y"
            + "es, answer 'F8'. IF not, answer 'NOT F8'. Note that most of t"
            + "he problems related to power liftgate electrical problems and"
            + " rear view camera are NOT F8. Question 2: For each of these s"
            + "entences that your answer 1 was 'F8', check if it is related "
            + f"to only one of the following categories: {list(load_categories())}"
            + ". You should give only one answer with one answer for Questio"
            + "n 1 and one answer for Question 2 in the following format: 'A"
            + "NSWER 1~~~ANSWER 2'. Note: 'OWD' means 'opened while driving'"
            + " and 'F&F' means 'fit and finish', for problems related to fl"
            + "ushness and margin. Note 2: For model Escape (2020 forward), "
            + "there is a common problem related to door check arm when the "
            + "decription is related to the door making popping sounds, open"
            + "ing and closing problens, hinges and welds. If you cannot rel"
            + "ate, answer NOT SURE. Answer in the correct order. If you can"
            + "not assist, answer 1, and answer 2 must be NA. You should be "
            + "objective and cold. Never change the answer format mentioned."
        )
        content = {
            "model": "gpt-4",
            "context": (
                "You are a helpful text reader and analyzer. You need to give me 2 answers."
                + text
            ),  # sets the overall behavior of the assistant.
            "messages": [{"role": "user", "content": prompt + ", " + text}],
            "parameters": {
                "temperature": 0.05,  # Determines the randomnes of the model's response.
            },
        }
        try:
            response = httpx.post(
                self.credentials["url"],
                headers={"Authorization": f"Bearer {self.credentials['token']}"},
                json=content,
                timeout=360,
            )
        except Exception as exc:
            self.logger.exception(exc)
            raise TransformError(str(exc)) from Exception

        if response.status_code == 200:
            return self.__process_response(response.json()["content"])
        return "NOT CLASSIFIED"

    def __process_response(self, message: str) -> str:
        """
        Process response from ChatGPT, divide function, component and failure mode
        response format is: "Function~~~Result" where result is "component | failure"

        Args:
            data (str): api response message

        Returns:
            str: binning
        """
        message = message.split("\n")[0] if "\n" in message else message

        if len(parts := message.split("~~~")) == 2:
            function, result = parts

            if function == "NOT F8":
                return "~"

            if function == "F8":
                return result

        return "NOT CLASSIFIED"
