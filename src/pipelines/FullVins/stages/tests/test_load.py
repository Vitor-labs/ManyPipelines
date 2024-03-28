"""
Test case for transformion step
"""

from typing import Any, Generator, NoReturn

import pytest
from dotenv import load_dotenv, find_dotenv

from src.errors.load_error import LoadError
from src.pipelines.FullVins.stages.load import DataLoader


@pytest.fixture(name="test_setup")
def setup() -> Generator[DataLoader, Any, Any]:
    """
    Test basic setup to prepare for next cases, create the basic flow of
    loading

    Yields:
        DataLoader: Data loader instance
    """
    load_dotenv(find_dotenv())
    yield DataLoader()


def test_transform_success(test_setup) -> NoReturn:
    """
    Test case for DataLoader.load_data sucess
    """
    loader = test_setup

    try:
        # TODO: need to implement mock for transform contract
        loader.load_data()
    except LoadError as exc:
        pytest.fail(f"FAILED: {exc}")


def test_load_fail(test_setup) -> NoReturn:
    """
    Test case for DataLoader.load_data fail and raise exception
    """
    transformor = test_setup
    with pytest.raises(LoadError):
        # TODO: need to implement mock for transform contract
        transformor.load_data()
