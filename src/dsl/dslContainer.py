from typing import List, Optional

from pydantic import BaseModel, Field
from dsl.dslDataType import DslDataType
from dsl.dslValue import DslValue

class DslContainer(BaseModel):
    """Represents a container for a node's value."""

    dataType: DslDataType = Field(description="Data type of the node")
    value: Optional[DslValue] = Field(default=None, description="What is value of this node. Applicable if data can be directly defined")
    children: Optional[List["Mapping"]] = Field(default=None, description="List of children nodes if node is a complex object or array. This will be applicable in case of datatype OBJECT OR LIST")

from dsl.mapping import Mapping