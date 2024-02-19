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
from src.errors.extract_error import ExtractError
from src.pipelines.NHTSA_VOQs.contracts.schemas.extract import schema
from src.pipelines.NHTSA_VOQs.contracts.extract_contract import ExtractContract
from src.utils.funtions import create_client


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

    def __mount_dataset_from_content(self, info: Dict) -> pd.DataFrame:
        self.logger.debug("\nMounting extracted Dataset")

        if date.strftime(info["updated_date"], "%Y-%m-%d") >= str(
            os.getenv("LAST_COMPLAINT_WAVE_DATE")
        ):
            raise ExtractError("Datasets not updated")

        with create_client() as client:
            resp = client.get(info["url"], timeout=160).content

        with ZipFile(BytesIO(resp)) as myzip:
            with myzip.open("COMPLAINTS_RECEIVED_2020-2024.txt") as file:
                dataset = pd.read_csv(file, sep="\t", header=None, names=self.columns)
                # dataset = schema.validate(df)

        df = dataset[
            (dataset["MFR_NAME"] == "Ford Motor Company")
            & (
                pd.to_datetime(dataset["DATEA"], format="%Y%m%d")
                > pd.Timestamp(str(os.getenv("LAST_COMPLAINT_WAVE_DATE")))
            )
            & (dataset["YEARTXT"].fillna(0).astype(int) > 2011)
        ]

        df.to_csv("./data/raw/mock_complaints.csv")

        return dataset

    def __extract_links_from_page(self, url) -> List:
        with create_client() as client:
            self.logger.info("Acessing NHSTA datasets...")
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
