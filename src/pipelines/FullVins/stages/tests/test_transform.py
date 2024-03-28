"""
Test case for transformion step
"""

from typing import Any, Generator, NoReturn

import pytest
from pandas import DataFrame
from dotenv import load_dotenv, find_dotenv

from src.errors.transform_error import TransformError
from src.contracts.transform_contract import TransformContract
from src.pipelines.FullVins.stages.transform import DataTransformer


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


@pytest.mark.asyncio
async def test_transform_success(test_setup) -> NoReturn:
    """
    Test case for HttpRequest.transform sucess
    """
    transformer = test_setup

    try:
        # TODO: need to implement mock for extract contract
        response = await transformer.transform()
    except TransformError as exc:
        pytest.fail(f"FAILED: {exc}")

    assert isinstance(response, TransformContract)
    assert isinstance(response.raw_data, DataFrame)


@pytest.mark.asyncio
async def test_transform_fail(test_setup) -> NoReturn:
    """
    Test case for DataTransformer.transform fail and raise exception
    """
    transformor = test_setup
    with pytest.raises(TransformError):
        # TODO: need to implement failing mock for extract contract
        await transformor.transform()
