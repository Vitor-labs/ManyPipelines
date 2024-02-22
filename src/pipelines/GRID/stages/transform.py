"""
This module defines the basic flow of data Tranformation from data
retrived from NHTSA.
"""

import os
import time
import logging
from typing import Dict, List
from functools import lru_cache
from src.utils.funtions import load_classifier_credentials


from src.utils.logger import setup_logger
from src.errors.transform_error import TransformError
from src.pipelines.GRID.contracts.extract_contract import ExtractContract
from src.pipelines.GRID.contracts.transform_contract import TransformContract


class DataTransformer:
    """
    Class to define the flow of the data transformation step.

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

        credentials = load_classifier_credentials()
        processeds = []
        # TODO: get real car model
        # TODO: binning
        for issue in new_issues:
            issue["Affected Vehicles"] = self.__resume_vehicle(
                issue["Affected Vehicles"]
            )
            issue["Binning"] = self.__classify_case(issue[["", ""]], credentials)

        return processeds

    def __resume_vehicle(self, vehicle: str) -> str:
        return vehicle

    @retry([Exception])
    @rate_limiter(70, 1)
    @lru_cache(maxsize=70)
    def __classify_case(self, complaint: str, url: str, token: str) -> List[str]:
        """
        Uses ChatGPT-4.0 to classify each recall by failure mode

        Args:
            decription (str): complaint description
            url (str): api endpoint
            token (str): authorization token

        Raises:
            exc: ConnectionError, API not responded

        Returns:
            str: result of classificaiton (failure mode)
        """
        parts = (
            "door, window, windshield, wiper, glass, hood, trunk, moonroof, "
            + "bumper, tail light, pillar, undershield, roof rack, latch, he"
            + "adlight, door handle, door keypad, window, weatherstripping, "
            + "side mirror, lighting, swing gate, cowl grille, hard top, ski"
            + "d plate, sheet metal, running boards, water leak, etc"
        )
        text = (
            "Question 1: For this complaint, check if it is related to an ex"
            + f"ternal part of the car, body exterior, ({parts}). If yes, an"
            + "swer 'F8'. Otherwise, answer 'NOT F8'. Note that most of the "
            + "problems related to power liftgate electrical problems and re"
            + "ar view camera are NOT F8. Question 2: For each of these sent"
            + "ences that your answer 1 was 'F8', check if it is related to "
            + f"only one of the following categories: {list(categories)}. Yo"
            + "u should give only one answer with one answer for Question 1 "
            + "and one answer for Question 2 in the following format: 'ANSWE"
            + "R 1~~~ANSWER 2'. Note: 'OWD' means 'opened while driving' and"
            + "'F&F' means 'fit and finish', for problems related to flushne"
            + "ss and margin. Note 2: For model Escape (2020 forward), there"
            + " is a common problem related to door check arm when the compl"
            + "aint is related to the door making popping sounds, opening an"
            + "d closing problens, hinges and welds. If you cannot relate, a"
            + "nswer NOT SURE. Answer in the correct order. If you cannot as"
            + "sist, answer 1, and answer 2 must be NA. You should be object"
            + "ive and cold. Never change the answer format mentioned."
        )
        content = {
            "model": "gpt-4",
            "context": (
                "You are a helpful text reader and analyzer. You need to give me 2 answers."
            ),  # sets the overall behavior of the assistant.
            "messages": [{"role": "user", "content": complaint + text}],
            "parameters": {
                "temperature": 0.05,  # Determines the randomnes of the model's response.
            },
        }
        try:
            response = httpx.post(
                url,
                headers={"Authorization": f"Bearer {token}"},
                json=content,
                timeout=360,
            )
        except Exception as exc:
            self.logger.exception(exc)
            self.logger.error(exc)
            raise TransformError(str(exc)) from Exception

        if response.status_code == 200:
            return self.__process_response(
                response.content.decode("utf-8").split(":")[1].strip("}'").strip('"')
            )
        return ["NOT CLASSIFIED", "~", "~"]
