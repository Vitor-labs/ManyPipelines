"""
This module defines the contract to data transfering betwen the Extraction
and Transform Step. A named tuple representing the extracted data with:

1. raw_data: The raw dataset to be extracted.
2. extract_date: The date of extraction.
"""

from datetime import date
from typing import NamedTuple
from typing import List, Dict

ExtractContract = NamedTuple(
    "ExtractContract", [("raw_data", List[Dict[str, str]]), ("extract_date", date)]
)
