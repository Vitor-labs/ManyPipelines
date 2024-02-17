"""
This module defines some test cases for extracting a dataset from
nhtsa portal
"""

import pytest
from pandas import DataFrame

from src.errors.extract_error import ExtractError
from src.pipelines.NHTSA_VOQs.stages.extract import DataExtractor


def test_extract_sucess():
    """
    Test case for extracting sucess
    """
    try:
        extractor = DataExtractor()
        dataset = extractor.extract()

        assert isinstance(dataset, DataFrame)
    except ExtractError as exc:
        pytest.fail(f"Extract error catched: {exc}")
