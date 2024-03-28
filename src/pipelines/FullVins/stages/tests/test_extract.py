"""
Test case for extraction step
"""

from datetime import date
from typing import Any, Generator, NoReturn

import pytest
from pandas import DataFrame
from dotenv import load_dotenv, find_dotenv

from src.errors.extract_error import ExtractError
from src.contracts.extract_contract import ExtractContract
from src.pipelines.FullVins.stages.extract import DataExtractor


@pytest.fixture(name="test_setup")
def setup() -> Generator[DataExtractor, Any, Any]:
    """
    Test basic setup to prepare for next cases, create the basic flow
    of extration

    Yields:
        DataExtractor: Data Extractor instance
    """
    load_dotenv(find_dotenv())
    yield DataExtractor()


def test_extract_success(test_setup) -> NoReturn:
    """
    Test case for DataExtractor.extract success
    """
    extractor = test_setup

    try:
        response = extractor.extract()
    except ExtractError as exc:
        pytest.fail(f"FAILED: {exc}")

    assert isinstance(response, ExtractContract)
    assert isinstance(response.raw_data, DataFrame)
    assert response.extract_date == date.today()


def test_extract_fail(test_setup) -> NoReturn:
    """
    Test case for DataExtract.extract fail and raise exception
    """
    extractor = test_setup
    with pytest.raises(ExtractError):
        extractor.extract("_")  # type: ignore
