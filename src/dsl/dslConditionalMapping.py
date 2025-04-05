from typing import List, Optional

from pydantic import BaseModel, Field
from src.dsl.mapping import Mapping
from src.dsl.dslCondition import DslCondition
from src.dsl.dslValue import DslValue

class DslConditionalMapping(BaseModel):
    """The parent class for all DSL conditional mappings."""
    
    condition: Optional[DslCondition] = Field(default=None, description="Condition for the mapping")
    mappingList: List[Mapping] = Field(
        description="List of mappings to apply"
    )
    stringMapping: Optional[DslValue] = Field(default=None, description="String mapping value")