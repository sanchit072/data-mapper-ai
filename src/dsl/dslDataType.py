from typing import List
from enum import Enum
from pydantic import Field

class DslDataType(str, Enum):
    """Represents the data type of a node."""

    STRING = "STRING"
    INT = "INT"
    BOOL = "BOOL"
    OBJECT = "OBJECT"
    LIST = "LIST"
    