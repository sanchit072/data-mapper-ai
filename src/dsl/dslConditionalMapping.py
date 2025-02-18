from typing import List

from pydantic import BaseModel, Field
from dsl.mapping import Mapping

class DslConditionalMapping(BaseModel):
    """The parent class for all DSL conditional mappings."""
    
    mappingList: List[Mapping] = Field(
        description="List of mappings of all nodes"
    )