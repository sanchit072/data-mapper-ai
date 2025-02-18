from typing import List

from pydantic import BaseModel, Field
from dsl.dslDataType import DslDataType
from dsl.dslValue import DslValue
from dsl.mapping import Mapping

class DslContainer(BaseModel):
    """Represents a container for a node's value."""

    dataType: DslDataType = Field(description="Data type of the node")
    value: DslValue = Field(description="What is value of this node. Applicable if data can be directly defined")
    children: List[Mapping] = Field(description="List of children nodes if node is a complex object or array. This will be applicable in case of datatype OBJECT OR LIST")