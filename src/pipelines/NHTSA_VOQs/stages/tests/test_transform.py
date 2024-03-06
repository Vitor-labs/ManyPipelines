"""
This module defines some test cases for extracting a dataset from
nhtsa portal
"""

from datetime import date

import pytest
import pandas as pd
from dotenv import load_dotenv, find_dotenv

from src.errors.transform_error import TransformError
from src.pipelines.NHTSA_VOQs.stages.transform import DataTransformer
from src.pipelines.NHTSA_VOQs.contracts.extract_contract import ExtractContract
from src.pipelines.NHTSA_VOQs.contracts.transform_contract import TransformContract


@pytest.fixture
def setup() -> ExtractContract:
    """
    test setup mocking the data extraction step

    Returns:
        pd.DataFrame: collected dataset from nhtsa
    """
    load_dotenv(find_dotenv())

    mock = pd.read_csv("./data/raw/mock_dataset.csv")

    return ExtractContract(
        raw_data=mock[mock["MFR_NAME"] == "Ford Motor Company"],
        extract_date=date(2024, 2, 22),
    )


@pytest.mark.asyncio
async def test_transform_sucess(setup: ExtractContract) -> None:
    """
    Test case for transforming sucess
    """
    try:
        tranformer = DataTransformer()
        dataset = await tranformer.transform(contract=setup)

        assert isinstance(dataset, TransformContract)
        assert "PROD_DATE" in dataset.content.columns

        dataset.content.to_csv("./data/raw/tranformed_dataset_mock.csv")

    except TransformError as exc:
        pytest.fail(f"Extract error catched: {exc}")
