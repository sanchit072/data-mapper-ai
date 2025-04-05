from typing import List
from pydantic import BaseModel, Field
from src.dsl.dslFunction import DslFunction
from src.dsl.dslContainer import DslContainer

class DslTransformation(BaseModel):
    """Represents a data transformation in the DSL."""
    
    function: DslFunction = Field(description="Function to apply for transformation")
    containerList: List[DslContainer] = Field(description="List of containers to transform") 