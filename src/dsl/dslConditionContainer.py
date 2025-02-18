from typing import List

from pydantic import BaseModel, Field
from dsl.dslContainer import DslContainer
from dsl.dslCondition import DslCondition

class DslConditionContainer(BaseModel):
    """The class which contains the condition and the container to be applied if the condition is true."""

    container: DslContainer = Field(
        description="Container for the value of a node"
    )
    condition: DslCondition = Field(
        description="DslCondition if true, above container will be applied"
    )
    
    