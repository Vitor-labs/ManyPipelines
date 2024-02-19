"""
This module defines the basic flow of data Extraction from NHTSA portal
"""

import os
import time
import logging

from io import BytesIO
from zipfile import ZipFile
from datetime import datetime
from typing import Dict, List

import bs4
import httpx
import pandas as pd
import pandera as pa

from src.utils.decorators import retry
from src.utils.logger import setup_logger
from src.errors.extract_error import ExtractError
from src.pipelines.NHTSA_VOQs.schemas.extract import schema


class DataExtractor:
    """
    Class to define the flow of the data extraction step.
    1. Request dataset file from url
    2. Mounts the dataset as a pandas DataFrame
    3. Filters what's new and returns.
    """

    def __init__(self) -> None:
        self.columns = [
            "CMPLID",
            "ODINO",
            "MFR_NAME",
            "MAKETXT",
            "MODELTXT",
            "YEARTXT",
            "CRASH",
            "FAILDATE",
            "FIRE",
            "INJURED",
            "DEATHS",
            "COMPDESC",
            "CITY",
            "STATE",
            "VIN",
            "DATEA",
            "LDATE",
            "MILES",
            "OCCURENCES",
            "CDESCR",
            "CMPL_TYPE",
            "POLICE_RPT_YN",
            "PURCH_DT",
            "ORIG_OWER_YN",
            "ANTI_BRAKES_YN",
            "CRUISE_CONT_YN",
            "NUM_CYLS",
            "DRIVE_TRAIN",
            "FUEL_SYS",
            "FUEL_TYPE",
            "TRASN_TYPE",
            "VEH_SPEED",
            "DOT",
            "TIRE_SIZE",
            "LOC_OF_TIRE",
            "TIRE_FAIL_TYPE",
            "ORIG_EQUIP_YN",
            "MANUF_DT",
            "SEAT_TYPE",
            "RESTRAINT_TYPE",
            "DEALER_NAME",
            "DEALER_TEL",
            "DEALER_CITY",
            "DEALER_STATE",
            "DEALER_ZIP",
            "PROD_TYPE",
            "REPAIRED_YN",
            "MEDICAL_ATTN",
            "VEHICLES_TOWED_YN",
        ]
        self.logger = logging.getLogger(__name__)
        setup_logger()

    @retry([ConnectionError])
    def extract(self) -> pd.DataFrame:
        """
        Main method of extraction

        Raises:
            ExtractError: error occurred during extraction

        Returns:
            ExtractContract: data extracted
        """
        start_time = time.time()
        self.logger.debug("\nRunning Extract stage")
        try:
            datasets = self.__extract_links_from_page(
                str(os.getenv("NHTSA_DATASETS_URL"))
            )
            return self.__mount_dataset_from_content(datasets[0])

        except Exception as exc:
            raise ExtractError(str(exc)) from exc

        finally:
            self.logger.debug("--- %s seconds ---", round(time.time() - start_time, 2))

    def __mount_dataset_from_content(self, info: Dict) -> pd.DataFrame:
        self.logger.debug("\nMounting extracted Dataset")

        if info["updated_date"] < datetime.now():
            resp = httpx.get(info["url"], timeout=160).content
            with ZipFile(BytesIO(resp)) as myzip:
                with myzip.open("COMPLAINTS_RECEIVED_2020-2024.txt") as file:
                    df = pd.read_csv(file, sep="\t", header=None, names=self.columns)
                    # dataset = schema.validate(df)
        return dataset[
            (dataset["MFR_NAME"] == "Ford Motor Company")
            & (
                pd.to_datetime(dataset["DATEA"], format="%Y%m%d")
                > pd.Timestamp("2024-02-01")
            )
        ]

    def __extract_links_from_page(self, url) -> List:
        soup = bs4.BeautifulSoup(httpx.get(url).text, "html.parser")
        tables = soup.select("#nhtsa_s3_listing > tbody")

        complaints = tables[3]
        elements = list(complaints.find_all("td"))
        data_list = []

        if len(elements) % 3 != 0:
            self.logger.warning(
                "The list of elements does not contain complete data for each row."
            )
        else:
            for i in range(0, len(elements), 3):
                url_elem = elements[i].find("a")
                size_elem = elements[i + 1]
                date_elem = elements[i + 2]

                data_dict = {
                    "url": url_elem.get("href") if url_elem else None,
                    "size": size_elem.text.strip() if size_elem else None,
                    "updated_date": (
                        datetime.strptime(
                            date_elem.text.strip(" ET"), "%m/%d/%Y %I:%M:%S %p"
                        )
                        if date_elem
                        else None
                    ),
                }
                data_list.append(data_dict)
        return data_list
