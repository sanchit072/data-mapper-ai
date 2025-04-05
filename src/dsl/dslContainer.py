from typing import List, Optional

from pydantic import BaseModel, Field
from src.dsl.dslDataType import DslDataType
from src.dsl.dslValue import DslValue
from src.dsl.dslForEach import DslForEach

class DslContainer(BaseModel):
    """Represents a container for a node's value."""

    forEach: Optional[DslForEach] = Field(default=None, description="For-each loop configuration")
    dataType: DslDataType = Field(description="Data type of the node")
    value: Optional[DslValue] = Field(default=None, description="What is value of this node. Applicable if data can be directly defined")
    children: Optional[List["Mapping"]] = Field(default=None, description="List of children nodes if node is a complex object or array. This will be applicable in case of datatype OBJECT OR LIST")
    container: Optional["DslContainer"] = Field(default=None, description="Nested container")

from src.dsl.mapping import Mapping