from typing import List, Optional

from pydantic import BaseModel, Field
from src.dsl.dslCondition import DslCondition

class DslConditionContainer(BaseModel):
    """The class which contains the condition and the container to be applied if the condition is true."""

    container: "DslContainer" = Field(
        description="Container for the value of a node"
    )
    condition: Optional[DslCondition] = Field(
        default=None,
        description="DslCondition if true, above container will be applied"
    )

from src.dsl.dslContainer import DslContainer
    
    