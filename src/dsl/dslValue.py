from typing import List, Optional

from pydantic import BaseModel, Field
from src.dsl.dslBase import DslBase

class DslValue(BaseModel):
    """Represents the value of a node."""

    base : Optional[DslBase] = Field(default=None, description="Base value from which xpath and jsonpath will be taken. For CSV files, this is always INTERACTION_1_RESPONSE_BODY if we are applying carrier mapping. For constant mappings, it is always NO_BASE")
    xpath: Optional[str] = Field(default=None, description="Path in xml used to assign value. Always applicable for CSV files")
    constantValue: Optional[str] = Field(default=None, description="Constant value to be assigned to the node. Applicable for all data types")
    translation: Optional[str] = Field(default=None, description="Assigning value using translation table.")
    transformation: Optional[str] = Field(default=None, description="Transformation in form of functions to be used for calculation.")

    
    
