from typing import Optional
from pydantic import BaseModel, Field
from src.dsl.dslBase import DslBase

class DslForEach(BaseModel):
    """Represents a for-each loop construct in the DSL."""
    
    base: DslBase = Field(description="Base value for iteration")
    jsonpath: Optional[str] = Field(default=None, description="JSONPath expression for iteration")
    xpath: Optional[str] = Field(default=None, description="XPath expression for iteration") 