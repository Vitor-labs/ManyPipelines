"""
This module defines the basic flow of data Tranformation from data
retrived from NHTSA.
"""

import os
import time
import logging
from typing import Dict, List
from functools import lru_cache

import httpx
import pandas as pd

from src.errors.transform_error import TransformError
from src.pipelines.NHTSA_VOQs.contracts.extract_contract import ExtractContract
from src.pipelines.NHTSA_VOQs.contracts.transform_contract import TransformContract

from src.utils.decorators import rate_limiter, retry
from src.utils.funtions import (
    load_categories,
    convert_code_into_state,
    get_quarter,
    get_mileage_class,
    classify_binning,
    load_vfgs,
    create_client,
)
from src.utils.logger import setup_logger


class DataTransformer:
    """
    Class to define the flow of the data transformation step

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
            return TransformContract(content=self.__transform_complaints(contract))
        except TransformError as exc:
            self.logger.exception(exc)
            raise exc
        finally:
            self.logger.info("--- %s minutes ---", round(time.time() - start_time, 2))

    def __transform_complaints(self, contract: ExtractContract) -> pd.DataFrame:
        """
        increments the dataset with addtional columns
        Args:
            contract (ExtractContract): dataset collected

        Returns:
            List[TransformedDataset]: list of dict, alike a pandas dataframe
        """
        transformed = pd.DataFrame(contract.raw_data)
        credentials = self.__load_classifier_credentials()
        vfgs = load_vfgs()
        gsar_token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsIng1dCI6ImFSZ2hZU01kbXI2RFZpMTdWVVJtLUJlUENuayJ9.eyJhdWQiOiJ1cm46Z3NhcjpyZXNvdXJjZTp3ZWI6cHJvZCIsImlzcyI6Imh0dHBzOi8vY29ycC5zdHMuZm9yZC5jb20vYWRmcy9zZXJ2aWNlcy90cnVzdCIsImlhdCI6MTcwODM2ODY3NSwiZXhwIjoxNzA4Mzk3NDc1LCJDb21tb25OYW1lIjoiVkRVQVJUMTAiLCJzdWIiOiJWRFVBUlQxMCIsInVpZCI6InZkdWFydDEwIiwiZm9yZEJ1c2luZXNzVW5pdENvZGUiOiJGU0FNUiIsImdpdmVuTmFtZSI6IlZpY3RvciIsInNuIjoiRHVhcnRlIiwiaW5pdGlhbHMiOiJWLiIsIm1haWwiOiJ2ZHVhcnQxMEBmb3JkLmNvbSIsImVtcGxveWVlVHlwZSI6Ik0iLCJzdCI6IkJBIiwiYyI6IkJSQSIsImZvcmRDb21wYW55TmFtZSI6IklOU1QgRVVWQUxETyBMT0RJIE4gUkVHSU9OQUwgQkFISUEiLCJmb3JkRGVwdENvZGUiOiIwNjY0Nzg0MDAwIiwiZm9yZERpc3BsYXlOYW1lIjoiRHVhcnRlLCBWaWN0b3IgKFYuKSIsImZvcmREaXZBYmJyIjoiUFJEIiwiZm9yZERpdmlzaW9uIjoiUEQgT3BlcmF0aW9ucyBhbmQgUXVhbGl0eSIsImZvcmRDb21wYW55Q29kZSI6IjAwMDE1ODM4IiwiZm9yZE1hbmFnZXJDZHNpZCI6Im1tYWdyaTEiLCJmb3JkTVJSb2xlIjoiTiIsImZvcmRTaXRlQ29kZSI6IjY1MzYiLCJmb3JkVXNlclR5cGUiOiJFbXBsb3llZSIsImFwcHR5cGUiOiJQdWJsaWMiLCJhcHBpZCI6InVybjpnc2FyOmNsaWVudGlkOndlYjpwcm9kIiwiYXV0aG1ldGhvZCI6Imh0dHA6Ly9zY2hlbWFzLm1pY3Jvc29mdC5jb20vd3MvMjAwOC8wNi9pZGVudGl0eS9hdXRoZW50aWNhdGlvbm1ldGhvZC93aW5kb3dzIiwiYXV0aF90aW1lIjoiMjAyNC0wMi0xOVQxODo1NjoxNS4zNThaIiwidmVyIjoiMS4wIn0.hrND9dXaq0yTK8D7970t2u1LaHRp9DL5gBPPaQXqJD9BJnBHt8QjHNiFxDo4Cw_7qf-ur3Ofp-2b94-bIF3z8W17xGQUhUWlmmAWdueU4jfDxt264vpQv3eOvh2JOnldTA6s3IzJMaPmO_6iVssj6rH-7nc_2jGez59tCIiSRAnW2fojkcU9ZI9ibVOBXvAZH5HIv7a2GNsQDc7gmbfaVEJ0pE141uOAIRlzbhFFE9qtW2byi7V_CnaONie4LOwW7pl9IVz2aHiHr9I3cj_otGp31c1YtgIYjPQDrBb3MN6aPvCtZrZgE88IqxvGrRNc1DKKgDEuMMzAvRmszs-VAg"

        transformed[["FUNCTION_", "COMPONET", "FAILURE"]] = transformed.apply(
            lambda row: self.__classify_case(row["CDESCR"], credentials),
            axis=0,
            result_type="expand",
        )
        transformed["BINNING"] = transformed.apply(
            lambda row: row["COMPONET"] + " | " + row["FAILURE"], axis=0
        )
        transformed["FULL_STATE"] = transformed.apply(
            lambda row: convert_code_into_state(row["STATE_"]), axis=0
        )
        transformed["FAIL_QUARTER"] = transformed.apply(
            lambda row: get_quarter(row["FAIL_DATE"]),
            axis=0,
        )
        transformed["VFG"] = transformed.apply(lambda row: vfgs[row["BINNING"]], axis=0)
        transformed["FULL_VIN"] = ""
        transformed[
            [
                "PROD_DATE",
                "VEHICLE_LINE_WERS",
                "VEHICLE_LINE_GSAR",
                "VEHICLE_LINE_GLOBAL",
                "ASSEMBLY_PLANT",
                "WARRANTY_START_DATE",
            ]
        ] = transformed.apply(
            lambda row: self.__get_info_by_vin(row["FULL_VIN"], gsar_token),
            axis=0,
            result_type="expand",
        )
        transformed["REPAIR_DATE_1"] = ""
        transformed["REPAIR_DATE_2"] = ""
        transformed["FAILURE_MODE"] = transformed.apply(
            lambda row: classify_binning(row["BINNING"]), axis=0
        )
        transformed["MILEAGE_CLASS"] = transformed.apply(
            lambda row: get_mileage_class(row["MILES"]), axis=0
        )
        transformed["EXTRACTED_DATE"] = contract.extract_date
        # TODO: remove this
        transformed.to_csv("tranformed_dataset_mock.csv")

        return transformed

    def __get_info_by_vin(self, vin: str, token: str) -> Dict[str, str]:
        response = httpx.get(
            str(os.getenv("GSAR_WERS_URL")),
            params={"vin": vin},
            headers={"Authorization": f"Bearer {token}"},
            proxies={
                "http": "http://internet.ford.com:83",
                "https": "http://internet.ford.com:83",
            },
        )
        data = dict(response.json())
        return {
            key: data[key]
            for key in [
                "prodDate",
                "wersVl",
                "awsVl",
                "globVl",
                "plant",
                "origWarantDate",
            ]
        }

    def __load_classifier_credentials(self) -> Dict[str, str]:
        """
        create a dict with classifier endpoint and auth.

        Returns:
            Dict[str, str]: _description_
        """
        with create_client() as client:
            response = client.post(
                str(os.getenv("TOKEN_ENDPOINT")),
                data={
                    "client_id": str(os.getenv("CLIENT_ID")),
                    "client_secret": str(os.getenv("CLIENT_SECRET")),
                    "scope": str(os.getenv("SCOPE")),
                    "grant_type": "client_credentials",
                },
                timeout=160,
            )
        return {
            "url": str(os.getenv("API_ENDPOINT")),
            "token": response.json()["access_token"],
        }

    @retry([Exception])
    @rate_limiter(70, 1)
    @lru_cache(maxsize=70)
    def __classify_case(self, complaint: str, credentials: Dict[str, str]) -> List[str]:
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
        categories = load_categories("Binnings")
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
            with create_client() as client:
                response = client.post(
                    credentials["url"],
                    headers={"Authorization": f"Bearer {credentials['token']}"},
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

    def __process_response(self, message: str) -> List[str]:
        """
        Process response from ChatGPT, divide function, component and failure mode
        response format is: "Function~~~Result" where result is "component | failure"

        Args:
            data (str): api response message

        Returns:
            List[str | float]: function, component, failure
        """
        if "\n" in message:
            message = message.split("\n")[0]

        if len(parts := message.split("~~~")) == 2:
            function, result = parts

            if function == "NOT F8":
                return [function, "~", "~"]

            if function == "F8":
                if "|" not in result:  # case where recalls is being processed
                    return [function, "~", result]

                component, failure = result.split(" | ")
                return [function, component, failure]

        return ["NOT CLASSIFIED", "~", "~"]
