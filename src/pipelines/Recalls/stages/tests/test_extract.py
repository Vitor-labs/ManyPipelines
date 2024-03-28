"""
This module defines some test cases for extracting a dataset from
nhtsa portal
"""

from datetime import date
from typing import Any, Generator, NoReturn

import pytest
from pandas import DataFrame
from dotenv import load_dotenv, find_dotenv

from src.errors.extract_error import ExtractError
from src.pipelines.Recalls.stages.extract import DataExtractor


@pytest.fixture(name="test_setup")
def setup() -> Generator[DataExtractor, Any, Any]:
    """
    Test basic setup to prepare for next cases, create the basic flow
    of extration

    Yields:
        DataExtractor: Data extractor instance
    """
    load_dotenv(find_dotenv())
    yield DataExtractor()


def test_extract_sucess(test_setup) -> NoReturn:
    """
    Test case for extracting sucess
    """
    try:
        extractor = test_setup
        dataset = extractor.extract()

        assert "NHTSA_ID" in dataset.raw_data.columns
        assert isinstance(dataset.raw_data, DataFrame)
        assert dataset.extract_date == date.today()

    except ExtractError as exc:
        pytest.fail(f"Extract error catched: {exc}")


def test_extract_fail(test_setup) -> NoReturn:
    """
    Test case for DataExtractor.extract fail and raise exception
    """
    extractor = test_setup
    with pytest.raises(ExtractError):
        extractor.extract("_")
