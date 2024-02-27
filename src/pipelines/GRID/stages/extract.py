"""
This module defines the basic flow of data Extraction from NHTSA portal
"""

import logging
import os
from typing import Dict, List
from datetime import date

import pandas as pd
from src.utils.decorators import time_logger

from src.utils.logger import setup_logger
from src.errors.extract_error import ExtractError
from src.pipelines.GRID.contracts.extract_contract import ExtractContract


class DataExtractor:
    """
    Class to define the flow of the data extraction step.
    1. Request dataset file from url
    2. Mounts the dataset as a pandas DataFrame
    3. Filters what's new and returns.
    """

    logger = logging.getLogger(__name__)
    setup_logger()

    def __init__(self) -> None:
        self.PATH = "C:/Users/VDUART10/azureford/CCM SA Team - GRID Issue Mgmt/GRID_Last_Update.xlsm"

    @time_logger(logger)
    def extract(self) -> ExtractContract:
        """
        Loads "GRID_Last_Update" as a dataset and returns only
        F8, North America, 2024 cases.

        Returns:
            pd.DataFrame: filtered dataframe
        """
        try:
            df = pd.read_excel(self.PATH, sheet_name="Data", dtype=str)

            filtered = df[
                (df["Function"].isin(["F8", "f8"]))
                & (df["Lead Region"] == "NA - North America")
                & (df["Issue #"].str.startswith("24-"))
            ]
            return ExtractContract(
                raw_data=self.__verify_new_issues(filtered), extract_date=date.today()
            )

        except FileNotFoundError as exc:
            raise ExtractError(str(exc)) from exc

    def __verify_new_issues(self, data: pd.DataFrame) -> List[Dict[str, str]]:
        """
        Verifies new issues from filtered data and returns the columns:
        "Issue #", "Issue Title", "Description", "Affected Vehicles",

        Args:
            data (pd.DataFrame): filtered dataframe

        Returns:
            List[Dict[str,str]]: new issue values
        """
        new_issues = []

        if data["Issue #"].iloc[0] == str(os.getenv("GRID_LAST_ISSUE")):
            raise ExtractError("No new issue found")

        for _, row in data.iterrows():
            if row["Issue #"] != "24-100":
                new_issues.append(
                    row[
                        [
                            "Function",
                            "Issue #",
                            "Issue Title",
                            "Description",
                            "Affected Vehicles",
                            "Days Open in CCRG",
                            "Days Open in CSF",
                            "Days Open in GOV",
                            "Days Open in EPRC",
                            "Field Service Action #",
                            "Overall Status",
                            "GRID creation date",
                        ]
                    ].to_dict()
                )
            else:
                break
        return new_issues
