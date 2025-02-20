from typing import List

from pydantic import BaseModel, Field

class DslCondition(BaseModel):
    """Represents the condition of a node."""

    operator: str = Field(description="Operator to be used for the condition")
    conditionParamList: List["DslConditionParam"] = Field(default=None,description="If it has more than 2 values, then also above operator will be applied on all of them.")

from src.dsl.dslConditionParam import DslConditionParam