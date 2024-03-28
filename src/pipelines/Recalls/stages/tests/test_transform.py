"""
This module defines some test cases for extracting a dataset from
nhtsa portal
"""

from typing import Any, Generator, NoReturn

import pytest
from dotenv import load_dotenv, find_dotenv

from src.errors.transform_error import TransformError
from src.contracts.transform_contract import TransformContract
from src.pipelines.Recalls.stages.transform import DataTransformer


@pytest.fixture(name="test_setup")
def setup() -> Generator[DataTransformer, Any, Any]:
    """
    Test basic setup to prepare for next cases, create the basic flow of
    transformation

    Yields:
        DataTransformer: Data transformer instance.
    """
    load_dotenv(find_dotenv())

    yield DataTransformer()


def test_transform_sucess(test_setup) -> NoReturn:
    """
    Test case for transforming sucess
    """
    transformer = test_setup

    try:
        dataset = transformer.transform()

        # TODO: need to implement mock for extract contract
        assert isinstance(dataset, TransformContract)
        assert "PROBLEM_ID" in dataset.content.columns

    except TransformError as exc:
        pytest.fail(f"Extract error catched: {exc}")


def test_transform_fail(test_setup) -> NoReturn:
    """
    Test case for DataTransformer.transform fail and raise exception
    """
    transformer = test_setup
    with pytest.raises(TransformError):
        # TODO: need to implement failing mock for extract contract
        transformer.transform()
