from typing import List
from pydantic import BaseModel, Field
from src.dsl.mapping import Mapping

class DslScript(BaseModel):
    """Represents a custom script in the DSL."""
    
    parameters: List[Mapping] = Field(description="Parameters for the script")
    code: str = Field(description="The script code to execute") 