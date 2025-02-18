from typing import List

from pydantic import BaseModel, Field
from dsl.dslContainer import DslContainer
from dsl.dslCondition import DslCondition

class DslConditionParam(BaseModel):
    """Represents the parameters for a condition. It can be simple value or a condition itself."""

    container: DslContainer = Field(description="Container containing value of the param.")
    condition: DslCondition = Field(description="Condition, in case this is nested.")
    
    