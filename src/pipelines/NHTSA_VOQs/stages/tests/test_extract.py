"""
This module defines some test cases for extracting a dataset from
nhtsa portal
"""

from dotenv import load_dotenv, find_dotenv
import pytest
from pandas import DataFrame

from src.errors.extract_error import ExtractError
from src.pipelines.NHTSA_VOQs.stages.extract import DataExtractor


def test_extract_sucess():
    """
    Test case for extracting sucess
    Test OK
    """
    load_dotenv(find_dotenv())

    try:
        extractor = DataExtractor()
        dataset = extractor.extract()

        assert "ODINO" in dataset.raw_data.columns
        assert isinstance(dataset.raw_data, DataFrame)

        dataset.raw_data.to_csv("./data/raw/mock_dataset.csv", index=False)

    except ExtractError as exc:
        pytest.fail(f"Extract error catched: {exc}")
