from typing import Optional

from pydantic import BaseModel, Field
from dsl.dslConditionalMapping import DslConditionalMapping
from typing import List

# Pydantic
class DslMapping(BaseModel):
    """The parent class for all DSL mappings."""

    format : str = "JSON"
    conditionalMappingList: List[DslConditionalMapping] = Field(description="List of all top level conditions, which if true, the underlying mapping will be applied.")