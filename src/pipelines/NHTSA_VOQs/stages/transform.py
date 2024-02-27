"""
This module defines the basic flow of data Tranformation from data
retrived from NHTSA.
"""

import os
import logging
from typing import List
from functools import lru_cache

import httpx
import pandas as pd

from src.errors.transform_error import TransformError
from src.pipelines.NHTSA_VOQs.contracts.extract_contract import ExtractContract
from src.pipelines.NHTSA_VOQs.contracts.transform_contract import TransformContract
from src.utils.logger import setup_logger
from src.utils.decorators import rate_limiter, retry, time_logger
from src.utils.funtions import (
    load_categories,
    convert_code_into_state,
    get_quarter,
    get_mileage_class,
    classify_binning,
    load_classifier_credentials,
    load_full_vins,
    load_new_models,
    load_vfgs,
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
            return TransformContract(content=self.__transform_complaints(contract))
        except TransformError as exc:
            self.logger.exception(exc)
            raise exc

    def __transform_complaints(self, contract: ExtractContract) -> pd.DataFrame:
        """
        increments the dataset with addtional columns
        Args:
            contract (ExtractContract): dataset collected

        Returns:
            List[TransformedDataset]: list of dict, alike a pandas dataframe
        """
        data = contract.raw_data
        vfgs = load_vfgs()
        vins = load_full_vins()
        new_models = load_new_models()
        credentials = load_classifier_credentials()
        gsar_token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsIng1dCI6ImFSZ2hZU01kbXI2RFZpMTdWVVJtLUJlUENuayJ9.eyJhdWQiOiJ1cm46Z3NhcjpyZXNvdXJjZTp3ZWI6cHJvZCIsImlzcyI6Imh0dHBzOi8vY29ycC5zdHMuZm9yZC5jb20vYWRmcy9zZXJ2aWNlcy90cnVzdCIsImlhdCI6MTcwOTAzNDIwNywiZXhwIjoxNzA5MDYzMDA3LCJDb21tb25OYW1lIjoiVkRVQVJUMTAiLCJzdWIiOiJWRFVBUlQxMCIsInVpZCI6InZkdWFydDEwIiwiZm9yZEJ1c2luZXNzVW5pdENvZGUiOiJGU0FNUiIsImdpdmVuTmFtZSI6IlZpY3RvciIsInNuIjoiRHVhcnRlIiwiaW5pdGlhbHMiOiJWLiIsIm1haWwiOiJ2ZHVhcnQxMEBmb3JkLmNvbSIsImVtcGxveWVlVHlwZSI6Ik0iLCJzdCI6IkJBIiwiYyI6IkJSQSIsImZvcmRDb21wYW55TmFtZSI6IklOU1QgRVVWQUxETyBMT0RJIE4gUkVHSU9OQUwgQkFISUEiLCJmb3JkRGVwdENvZGUiOiIwNjY0Nzg0MDAwIiwiZm9yZERpc3BsYXlOYW1lIjoiRHVhcnRlLCBWaWN0b3IgKFYuKSIsImZvcmREaXZBYmJyIjoiUFJEIiwiZm9yZERpdmlzaW9uIjoiUEQgT3BlcmF0aW9ucyBhbmQgUXVhbGl0eSIsImZvcmRDb21wYW55Q29kZSI6IjAwMDE1ODM4IiwiZm9yZE1hbmFnZXJDZHNpZCI6Im1tYWdyaTEiLCJmb3JkTVJSb2xlIjoiTiIsImZvcmRTaXRlQ29kZSI6IjY1MzYiLCJmb3JkVXNlclR5cGUiOiJFbXBsb3llZSIsImFwcHR5cGUiOiJQdWJsaWMiLCJhcHBpZCI6InVybjpnc2FyOmNsaWVudGlkOndlYjpwcm9kIiwiYXV0aG1ldGhvZCI6Imh0dHA6Ly9zY2hlbWFzLm1pY3Jvc29mdC5jb20vd3MvMjAwOC8wNi9pZGVudGl0eS9hdXRoZW50aWNhdGlvbm1ldGhvZC93aW5kb3dzIiwiYXV0aF90aW1lIjoiMjAyNC0wMi0yN1QxMTo0ODoyNy43MzlaIiwidmVyIjoiMS4wIn0.URSkqpedgPlC0madANL-Mmt5KpSIMmiVXbLn_wvaHMmb0pHgPHYs6IyQHG_b4ZyosRwQWRkk6zDtm223YjLEnxMZ5zqGt8zMAQK-khAB8PUKrQZG6rYDEKCXGd6VApUmKIiL10aS_JXj3q4i8EYsB5dR5cjjtCdGS0enXFy7b1y9V6p0_xk9mnIoXRnMMz_CmNTMehNdZ98Qn79lOjTga0LgG6MM9TIwevM6IkmGwPoTq0QHTRiSrlvRSOs8DtFsI2P_20WSqIp_-rG-e__rEW6H3g20lnC8EeYdPwYDSMUib2Xnk-zaQWK0Op4GIBhnqomwcguIFCllrKeR87d-uw"

        data["MODELTXT"].replace(new_models)
        data["FULL_STATE"] = data["STATE"].apply(convert_code_into_state)
        data["FAIL_QUARTER"] = data["FAILDATE"].apply(get_quarter)
        data["FULL_VIN"] = data["ODINO"].apply(lambda x: vins.get(x, " ~ "))
        data[["FUNCTION_", "COMPONET", "FAILURE"]] = (
            data["CDESCR"]
            .apply(
                lambda row: self.__classify_case(
                    row, credentials["url"], credentials["token"]
                )
            )
            .to_list()
        )
        data["BINNING"] = data["COMPONET"] + " | " + data["FAILURE"]
        data["VFG"] = data["BINNING"].apply(lambda x: vfgs.get(x, " ~ "))
        data["FAILURE_MODE"] = data["BINNING"].apply(classify_binning)
        data[
            [
                "PROD_DATE",
                "VEHICLE_LINE_WERS",
                "VEHICLE_LINE_GSAR",
                "VEHICLE_LINE_GLOBAL",
                "ASSEMBLY_PLANT",
                "WARRANTY_START_DATE",
            ]
        ] = (
            data["FULL_VIN"]
            .apply(lambda vin: self.__get_info_by_vin(vin, gsar_token))
            .to_list()
        )
        data["REPAIR_DATE_1"] = ""
        data["REPAIR_DATE_2"] = ""
        data["To_be_Binned"] = (
            data["MODELTXT"] + data["YEARTXT"].astype(str) + data["CDESCR"]
        )
        data["NewOld"] = ""
        data["New_Failure_Mode"] = ""
        data["MILEAGE_CLASS"] = data["MILES"].apply(get_mileage_class)
        data["EXTRACTED_DATE"] = contract.extract_date

        return data

    def __get_info_by_vin(self, vin: str, token: str) -> list[str]:
        keys = ["wersVl", "origWarantDate", "prodDate", "plant", "globVl", "awsVl"]
        retrived = dict.fromkeys(keys, "")

        if vin and vin[-1] != "*" and len(vin) == 17:
            response = httpx.get(
                str(os.getenv("GSAR_WERS_URL")),
                params={"vin": vin},
                headers={"Authorization": f"Bearer {token}"},
                proxies={
                    "http://": "http://internet.ford.com:83",
                    "https://": "http://internet.ford.com:83",
                },
            )
            data = dict(response.json())
            for key in keys:
                if key in data:
                    retrived[key] = str(data.get(key))

        return list(retrived.values())

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
        categories = load_categories("Binnings")
        text = (
            "Question 1: For this complaint, check if it's related to an ext"
            + f"ernal part of the car, body exterior, ({self.parts}). If yes"
            + ", answer 'F8'. IF not, answer 'NOT F8'. Note that most of the"
            + " problems related to power liftgate electrical problems and r"
            + "ear view camera are NOT F8. Question 2: For each of these sen"
            + "tences that your answer 1 was 'F8', check if it is related to"
            + f" only one of the following categories: {list(categories)}. Y"
            + "ou should give only one answer with one answer for Question 1"
            + " and one answer for Question 2 in the following format: 'ANSW"
            + "ER 1~~~ANSWER 2'. Note: 'OWD' means 'opened while driving' an"
            + "d 'F&F' means 'fit and finish', for problems related to flush"
            + "ness and margin. Note 2: For model Escape (2020 forward), the"
            + "re is a common problem related to door check arm when the com"
            + "plaint is related to the door making popping sounds, opening "
            + "and closing problens, hinges and welds. If you cannot relate,"
            + " answer NOT SURE. Answer in the correct order. If you cannot "
            + "assist, answer 1, and answer 2 must be NA. You should be obje"
            + "ctive and cold. Never change the answer format mentioned."
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
            raise TransformError(str(exc)) from Exception

        if response.status_code == 200:
            return self.__process_response(response.json()["content"])
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
                if "|" not in result:
                    return [function, "~", result]

                component, failure = result.split(" | ")
                return [function, component, failure]

        return ["NOT CLASSIFIED", "~", "~"]
