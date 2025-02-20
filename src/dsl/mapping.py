from typing import List

from pydantic import BaseModel, Field

class Mapping(BaseModel):
    """Represents a mapping node with conditions and output settings."""
    
    name: str = Field(description="Name of node")
    includeInOutput: bool = True
    conditionList: List["DslConditionContainer"] = Field(
        description="List of conditions & mapping to be applied for that condition"
    )

from src.dsl.dslConditionContainer import DslConditionContainer