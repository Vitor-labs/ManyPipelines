"""
This module defines the contract to data transfering betwen the Transform
and Loading Step. A named tuple representing the contract for transforming
data with:

1. content: The content to be transformed
"""

from typing import NamedTuple
from typing import List, Dict

TransformContract = NamedTuple("TransformContract", [("content", List[Dict[str, str]])])
