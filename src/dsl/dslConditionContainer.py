from typing import List, Optional

from pydantic import BaseModel, Field
from dsl.dslCondition import DslCondition

class DslConditionContainer(BaseModel):
    """The class which contains the condition and the container to be applied if the condition is true."""

    container: "DslContainer" = Field(
        description="Container for the value of a node"
    )
    condition: Optional[DslCondition] = Field(
        description="DslCondition if true, above container will be applied"
    )

from dsl.dslContainer import DslContainer
    
    