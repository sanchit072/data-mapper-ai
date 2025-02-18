from typing import List

from pydantic import BaseModel, Field
from dsl.dslConditionContainer import DslConditionContainer

class Mapping(BaseModel):
    """Represents a mapping node with conditions and output settings."""
    
    name: str = Field(description="Name of node")
    includeInOutput: bool = True
    conditionList: List[DslConditionContainer] = Field(
        description="List of conditions & mapping to be applied for that condition"
    )