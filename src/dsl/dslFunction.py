from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field

class PredefinedFunction(str, Enum):
    """Predefined functions available in the DSL."""
    
    LIBRARY = "LIBRARY"
    TO_LIST = "TO_LIST"
    REPLACE = "REPLACE"
    SPLIT = "SPLIT"
    NUMBER = "NUMBER"
    CONCAT = "CONCAT"
    SUBSTRING = "SUBSTRING"
    JOIN = "JOIN"
    INSERT = "INSERT"
    REMOVE = "REMOVE"
    TRIM = "TRIM"

class DslFunction(BaseModel):
    """Represents a function in the DSL."""
    
    predefinedFunction: Optional[PredefinedFunction] = Field(default=None, description="Predefined function to use")
    libraryFunction: Optional[str] = Field(default=None, description="Custom library function name") 