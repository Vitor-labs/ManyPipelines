"""
This module defines some test cases for extracting a dataset from
nhtsa portal
"""

from datetime import date

import pytest
import pandas as pd
from dotenv import load_dotenv, find_dotenv

from src.errors.transform_error import TransformError
from src.pipelines.NHTSA_VOQs.stages.extract import DataExtractor
from src.pipelines.NHTSA_VOQs.stages.transform import DataTransformer
from src.pipelines.NHTSA_VOQs.contracts.extract_contract import ExtractContract
from src.pipelines.NHTSA_VOQs.contracts.transform_contract import TransformContract


@pytest.fixture
def setup():
    """
    test setup mocking the data extraction step

    Returns:
        pd.DataFrame: collected dataset from nhtsa
    """
    load_dotenv(find_dotenv())

    mock = pd.read_csv("./data/raw/mock_complaints.csv")

    return ExtractContract(raw_data=mock, extract_date=date(2024, 2, 19))


def test_extract_sucess(setup):
    """
    Test case for transforming sucess
    """
    try:
        tranformer = DataTransformer()
        dataset = tranformer.transform(contract=setup)

        assert isinstance(dataset, TransformContract)
        assert "FUNCTION_" in dataset

    except TransformError as exc:
        pytest.fail(f"Extract error catched: {exc}")
