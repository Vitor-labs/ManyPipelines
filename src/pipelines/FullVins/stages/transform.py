"""
This module defines the basic flow of data Tranformation from data
retrived from NHTSA.
"""

import os
import logging
import asyncio
from typing import Tuple

import httpx
import pandas as pd

from src.utils.logger import setup_logger
from src.utils.funtions import create_async_client
from src.utils.decorators import retry, time_logger
from src.errors.transform_error import TransformError
from src.contracts.extract_contract import ExtractContract
from src.contracts.transform_contract import TransformContract


class DataTransformer:
    """
    Class to define the flow of the data transformation step

    methods:
        transform -> TransformContract: increase the dataset, adding columns
    """

    logger = logging.getLogger(__name__)
    setup_logger()

    def __init__(self) -> None:
        self.keys = [
            "prodDate",
            "wersVl",
            "awsVl",
            "globVl",
            "plant",
            "origWarantDate",
            "FuelType",
            "FuelTypeEng",
        ]

    @time_logger(logger=logger)
    async def transform(self, contract: ExtractContract) -> TransformContract:
        """
        Main flow to tranform data colleted from previews steps

        Args:
            contract (ExtractContract): contract with raw data to transform

        Raises:
            TransformError: Error occourin.g during this flow

        Returns:
            TransformContract: contract with transformed data to the next step
        """
        try:
            return TransformContract(content=await self.__process_vins_info(contract))
        except TransformError as exc:
            self.logger.exception(exc)
            raise exc

    async def __process_vins_info(self, contract: ExtractContract) -> pd.DataFrame:
        data = contract.raw_data

        gsar_token = self.__load_gsar_credential()
        async with create_async_client() as client:
            data[
                [
                    "PROD_DATE",
                    "VEHICLE_LINE_WERS",
                    "VEHICLE_LINE_GSAR",
                    "VEHICLE_LINE_GLOBAL",
                    "ASSEMBLY_PLANT",
                    "WARRANTY_START_DATE",
                    "FUEL_TYPE",
                    "FUEL_TYPE_ENG",
                ]
            ] = pd.DataFrame(
                await asyncio.gather(
                    *(
                        self.__get_info_by_vin(vin, client, gsar_token)
                        for vin in data["FULL_VIN"]
                    )
                )
            ).values
        data["PROD_DATE"] = (
            pd.to_datetime(data["PROD_DATE"], format="%d-%b-%Y", errors="coerce")
            .dt.strftime("%m/%d/%Y")
            .replace({"NaT": ""}, regex=True)
        )
        data["WARRANTY_START_DATE"] = (
            pd.to_datetime(
                data["WARRANTY_START_DATE"], format="%d-%b-%Y", errors="coerce"
            )
            .dt.strftime("%m/%d/%Y")
            .replace({"NaT": ""}, regex=True)
        )
        data["MODIFIED_AT"] = contract.extract_date
        return data

    def __load_gsar_credential(self) -> str:
        return (
            "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsIng1dCI6ImFSZ2hZU01kbXI2RFZ"
            + "pMTdWVVJtLUJlUENuayJ9.eyJhdWQiOiJ1cm46Z3NhcjpyZXNvdXJjZTp3ZWI"
            + "6cHJvZCIsImlzcyI6Imh0dHBzOi8vY29ycC5zdHMuZm9yZC5jb20vYWRmcy9z"
            + "ZXJ2aWNlcy90cnVzdCIsImlhdCI6MTcwOTczMTI4NCwiZXhwIjoxNzA5NzYwM"
            + "Dg0LCJDb21tb25OYW1lIjoiVkRVQVJUMTAiLCJzdWIiOiJWRFVBUlQxMCIsIn"
            + "VpZCI6InZkdWFydDEwIiwiZm9yZEJ1c2luZXNzVW5pdENvZGUiOiJGU0FNUiI"
            + "sImdpdmVuTmFtZSI6IlZpY3RvciIsInNuIjoiRHVhcnRlIiwiaW5pdGlhbHMi"
            + "OiJWLiIsIm1haWwiOiJ2ZHVhcnQxMEBmb3JkLmNvbSIsImVtcGxveWVlVHlwZ"
            + "SI6Ik0iLCJzdCI6IkJBIiwiYyI6IkJSQSIsImZvcmRDb21wYW55TmFtZSI6Ik"
            + "lOU1QgRVVWQUxETyBMT0RJIE4gUkVHSU9OQUwgQkFISUEiLCJmb3JkRGVwdEN"
            + "vZGUiOiIwNjY0Nzg0MDAwIiwiZm9yZERpc3BsYXlOYW1lIjoiRHVhcnRlLCBW"
            + "aWN0b3IgKFYuKSIsImZvcmREaXZBYmJyIjoiUFJEIiwiZm9yZERpdmlzaW9uI"
            + "joiUEQgT3BlcmF0aW9ucyBhbmQgUXVhbGl0eSIsImZvcmRDb21wYW55Q29kZS"
            + "I6IjAwMDE1ODM4IiwiZm9yZE1hbmFnZXJDZHNpZCI6Im1tYWdyaTEiLCJmb3J"
            + "kTVJSb2xlIjoiTiIsImZvcmRTaXRlQ29kZSI6IjY1MzYiLCJmb3JkVXNlclR5"
            + "cGUiOiJFbXBsb3llZSIsImFwcHR5cGUiOiJQdWJsaWMiLCJhcHBpZCI6InVyb"
            + "jpnc2FyOmNsaWVudGlkOndlYjpwcm9kIiwiYXV0aG1ldGhvZCI6InVybjpvYX"
            + "NpczpuYW1lczp0YzpTQU1MOjIuMDphYzpjbGFzc2VzOlBhc3N3b3JkUHJvdGV"
            + "jdGVkVHJhbnNwb3J0IiwiYXV0aF90aW1lIjoiMjAyNC0wMy0wNlQxMzoyNjoy"
            + "My45NzJaIiwidmVyIjoiMS4wIn0.kh7uPNLPrHmPCQ1xEE5tai2qyOCNwiPdm"
            + "zOYLZUFu0TzgauCWeRKKRFfmcwFErmFFe__NQyu5PrzViTHrZg9grr1KdLV7Q"
            + "xVSXjtLgkJOR0cNmII_PB_vi4qehUbeGHKiCaZW_zqs-V2eNDKAuLVeYdDeMI"
            + "Uw7bweJmL1DL3cpitETMKU3IfZDCf17Hnug_RxsXtwAh5uTtk4AdzQ7xlEAVY"
            + "kdwAX-kVCcahXhJxIZ2MzXpreVxfDBC8Ej-_2eoXu9l8EFkUr8ykr04WpWIbq"
            + "mIHO4VKau4nIltZPpqE99iYh24G-tubMuzJQ45hEBlGRozpxO-QhzscrTmdD1"
            + "G3GA"
        )

    @retry([Exception])
    async def __get_info_by_vin(
        self, vin: str, client: httpx.AsyncClient, token: str
    ) -> Tuple[str, str, str, str, str, str, str, str]:
        retrived = dict.fromkeys(self.keys, "")

        if vin != " ":
            response = await client.get(
                str(os.getenv("GSAR_WERS_URL")),
                params={"vin": vin},
                headers={"Authorization": f"Bearer {token}"},
            )
            data = dict(response.json())
            for key in self.keys:
                if key in data:
                    retrived[key] = str(data.get(key))

        return list(retrived.values())
