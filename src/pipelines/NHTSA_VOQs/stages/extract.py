"""
This module defines the basic flow of data Extraction from NHTSA portal
"""

import os
import time
import logging
from io import BytesIO
from zipfile import ZipFile
from typing import Dict, List
from datetime import date, datetime

import bs4
import pandas as pd
import pandera as pa

from src.utils.decorators import retry
from src.utils.logger import setup_logger
from src.utils.funtions import create_client
from src.errors.extract_error import ExtractError
from src.pipelines.NHTSA_VOQs.contracts.schemas.extract import schema
from src.pipelines.NHTSA_VOQs.contracts.extract_contract import ExtractContract


class DataExtractor:
    """
    Class to define the flow of the data extraction step.
    1. Request dataset file from url
    2. Mounts the dataset as a pandas DataFrame
    3. Filters what's new and returns.
    """

    def __init__(self) -> None:
        self.columns: List[str] = list(schema.columns.keys())
        self.logger = logging.getLogger(__name__)
        setup_logger()

    @retry([ConnectionError])
    def extract(self) -> ExtractContract:
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
            datasets = self.__extract_links_from_page(str(os.getenv("NHTSA_BASE_URL")))
            retrived = self.__mount_dataset_from_content(datasets[0])
            return ExtractContract(raw_data=retrived, extract_date=date.today())

        except Exception as exc:
            raise ExtractError(str(exc)) from exc

        finally:
            self.logger.debug("--- %s seconds ---", round(time.time() - start_time, 2))

    @pa.check_output(schema, lazy=True)
    def __mount_dataset_from_content(self, info: Dict) -> pd.DataFrame:
        self.logger.debug("\nMounting extracted Dataset")

        # if (updated_on := date.strftime(info["updated_date"], "%Y-%m-%d")) >= str(
        #     os.getenv("LAST_COMPLAINT_WAVE_DATE")
        # ):
        #     raise ExtractError(f"Datasets not updated on {updated_on}")

        with create_client() as client:
            resp = client.get(info["url"], timeout=160).content

        with ZipFile(BytesIO(resp)) as myzip:
            with myzip.open("COMPLAINTS_RECEIVED_2020-2024.txt") as file:
                df = pd.read_csv(file, sep="\t", header=None, names=self.columns)
                df.drop_duplicates(subset=["ODINO"], inplace=True)

                df["MILES"] = df["MILES"].fillna(0).astype(int)
                df["NUM_CYLS"] = df["NUM_CYLS"].fillna(0).astype(int)
                df["OCCURENCES"] = df["OCCURENCES"].fillna(0).astype(int)
                df["VEH_SPEED"] = df["VEH_SPEED"].fillna(0).astype(int)
                df["YEARTXT"] = df["MILES"].fillna(0).astype(int)

        return df[
            (df["MFR_NAME"] == "Ford Motor Company")
            & (
                pd.to_datetime(df["DATEA"], format="%Y/%m/%d")
                > pd.Timestamp(str(os.getenv("LAST_COMPLAINT_WAVE_DATE")))
            )
        ]

    def __extract_links_from_page(self, url) -> List:
        with create_client() as client:
            self.logger.debug("Acessing NHSTA datasets...")
            soup = bs4.BeautifulSoup(client.get(url).text, "html.parser")

        complaints = soup.select("#nhtsa_s3_listing > tbody")[3]
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
