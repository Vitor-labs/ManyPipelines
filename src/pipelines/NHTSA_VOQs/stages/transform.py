"""
This module defines the basic flow of data Tranformation from data
retrived from NHTSA.
"""

import logging
from functools import lru_cache

import httpx
import pandas as pd

from src.utils.logger import setup_logger
from src.errors.transform_error import TransformError
from src.contracts.extract_contract import ExtractContract
from src.contracts.transform_contract import TransformContract
from src.utils.decorators import rate_limiter, retry, time_logger
from src.utils.funtions import (
    load_classifier_credentials,
    get_state_names,
    get_mileage_class,
    load_categories,
    load_new_models,
    load_full_vins,
    get_quarter,
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
        self.categories = list(load_categories())
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

        Raises:
            TransformError: Error occourin.g during this flow

        Returns:
            TransformContract: contract with transformed data to the next step
        """
        data = contract.raw_data
        vins = load_full_vins()

        try:
            data["ODINO"] = data["ODINO"].astype("int64")
            data["MODELTXT"].replace(load_new_models())
            data["YEARTXT"] = data["YEARTXT"].astype("int64").replace(9999, None)
            data["MILES"] = data["MILES"].astype("int64")
            data["FAIL_QUARTER"] = data["FAILDATE"].apply(get_quarter)
            data["FULL_VIN"] = data["ODINO"].apply(lambda x: vins.get(x, " "))
            data["EXTRACTED_DATE"] = contract.extract_date.strftime("%m/%d/%Y")
            data["MILEAGE_CLASS"] = data["MILES"].apply(get_mileage_class)
            data["LDATE"] = pd.to_datetime(data["LDATE"], format="%Y%m%d").dt.strftime(
                "%m/%d/%Y"
            )
            data["FAILDATE"] = pd.to_datetime(
                data["FAILDATE"], format="%Y%m%d"
            ).dt.strftime("%m/%d/%Y")

            # Assigning foreing keys
            data["PROBLEM_ID"] = data["CDESCR"].apply(self.__classify_case)
            data["LOCATION_ID"] = data["STATE"].replace(get_state_names)
            data["RECALL_ID"] = "~"

            return TransformContract(content=data)
        except TransformError as exc:
            self.logger.exception(exc)
            raise exc

    @retry([Exception])
    @rate_limiter(70, 1)
    @lru_cache(maxsize=70)
    def __classify_case(self, complaint: str) -> str:
        """
        Uses ChatGPT-4.0 to classify each recall by failure mode

        Args:
            decription (str): complaint description
            url (str): api endpoint
            token (str): authorization token

        Raises:
            exc: ConnectionError, API not responded

        Returns:
            Tuple: result of classificaiton (failure mode)
        """
        text = (
            "Question 1: For this complaint, check if it's related to an ext"
            + f"ernal part of the car, body exterior, ({self.parts}). If yes"
            + ", answer 'F8'. IF not, answer 'NOT F8'. Note that most of the"
            + " problems related to power liftgate electrical problems and r"
            + "ear view camera are NOT F8. Question 2: For each of these sen"
            + "tences that your answer 1 was 'F8', check if it is related to"
            + f" only one of the following categories: {self.categories}. Yo"
            + "u should give only one answer with one answer for Question 1 "
            + "and one answer for Question 2 in the following format: 'ANSWE"
            + "R 1~~~ANSWER 2'. Note: 'OWD' means 'opened while driving' and"
            + " 'F&F' means 'fit and finish', for problems related to flushn"
            + "ess and margin. Note 2: For model Escape (2020 forward), ther"
            + "e is a common problem related to door check arm when the comp"
            + "laint is related to the door making popping sounds, opening a"
            + "nd closing problens, hinges and welds. If you cannot relate, "
            + "answer NOT SURE. Answer in the correct order. If you cannot a"
            + "ssist, answer 1, and answer 2 must be NA. You should be objec"
            + "tive and cold. Never change the answer format mentioned. If y"
            + "ou really cannot relate to any of the mentioned categories, p"
            + "lease create a new category following the standard 'PROBLEMAT"
            + "IC PART | PROBLEM'."
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
                self.credentials["url"],
                headers={"Authorization": f"Bearer {self.credentials['token']}"},
                json=content,
                timeout=120,
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
            Tuple: function, component, failure
        """
        if "\n" in message:
            message = message.split("\n")[0]

        if len(parts := message.split("~~~")) == 2:
            function, result = parts

            if function == "NOT F8":
                return ["~"]

            if function == "F8":
                return [result]

        return ["NOT CLASSIFIED"]
