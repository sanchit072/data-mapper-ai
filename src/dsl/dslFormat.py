from typing import Optional
from enum import Enum

from pydantic import BaseModel, Field

# Pydantic
class DslFormat(str, Enum):
    """Format options for DSL mapping."""
    
    JSON = "JSON"
    XML = "XML"
    STRING = "STRING"