"""
Script entry to run NHTSA_VOQs pipeline
"""

import pytest
from dotenv import find_dotenv, load_dotenv

from src.errors.load_error import LoadError
from src.errors.extract_error import ExtractError
from src.errors.transform_error import TransformError
from src.pipelines.NHTSA_VOQs.main.pipeline import Pipeline


@pytest.mark.asyncio
async def test_run_pipeline():
    """
    Test case success to running the pipeline
    """
    dotenv_file = find_dotenv()
    load_dotenv(dotenv_file)

    try:
        await Pipeline().run()

    except [ExtractError, TransformError, LoadError] as excinfo:
        pytest.fail(excinfo)
