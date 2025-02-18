from typing import List

from pydantic import BaseModel, Field
from dsl.dslConditionParam import DslConditionParam

class DslCondition(BaseModel):
    """Represents the condition of a node."""

    operator: str = Field(description="Operator to be used for the condition")
    conditionParamList: List[DslConditionParam] = Field(description="If it has more than 2 values, then also above operator will be applied on all of them.")