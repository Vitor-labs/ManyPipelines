"""
Script entry to run GRID pipeline
"""

import pytest
from dotenv import find_dotenv, load_dotenv

from src.errors.load_error import LoadError
from src.errors.extract_error import ExtractError
from src.errors.transform_error import TransformError
from src.pipelines.GRID.main.pipeline import Pipeline


def test_run_pipeline():
    """
    Test case success to running the pipeline
    """
    load_dotenv(find_dotenv())

    try:
        Pipeline().run()

    except [ExtractError, TransformError, LoadError] as excinfo:
        pytest.fail(excinfo)
