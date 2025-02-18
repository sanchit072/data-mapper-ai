from typing import List

from pydantic import BaseModel, Field
from dsl.dslBase import DslBase

class DslValue(BaseModel):
    """Represents the value of a node."""

    base : DslBase = Field(description="Base value from which xpath and jsonpath will be taken. For CSV files, this is always INTERACTION_1_RESPONSE_BODY if we are applying carrier mapping. For constant mappings, it is always NO_BASE")
    xpath: str = Field(description="Path in xml used to assign value. Always applicable for CSV files")
    constantValue: str = Field(description="Constant value to be assigned to the node. Applicable for all data types")
    translation: str = Field(description="Assigning value using translation table.")
    transformation: str = Field(description="Transformation in form of functions to be used for calculation.")

    
    
