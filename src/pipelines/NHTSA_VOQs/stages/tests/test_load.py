"""
This modeule defines a test case for loading the data
collected into a csv file a appending to a excel file
"""

from datetime import date
import os
import pytest
import pandas as pd
from dotenv import load_dotenv, find_dotenv

from src.errors.load_error import LoadError
from src.pipelines.NHTSA_VOQs.stages.load import DataLoader
from src.pipelines.NHTSA_VOQs.contracts.transform_contract import TransformContract


@pytest.fixture
def setup():
    """
    test setup mocking the data extraction step

    Returns:
        pd.DataFrame: collected dataset from nhtsa
    """
    load_dotenv(find_dotenv())

    mock = pd.read_csv("./data/raw/tranformed_dataset_mock.csv")

    return TransformContract(content=mock)


def test_load_sucess(setup):
    """
    Test case for transforming sucess
    """
    try:
        DataLoader().load_data(contract=setup)
        today = date.today().strftime("%Y-%m-%d")

        # test if lies where created
        assert os.path.isfile(
            # f"./data/processed/NHTSA_COMPLAINTS_PROCESSED_{today}.csv"
            "C:/Users/VDUART10/azureford/CCM SA Team - AMBIENTE TESTE/F8_All_v3.xlsm"
        )

    except LoadError as exc:
        pytest.fail(f"Extract error catched: {exc}")
