from typing import List, Optional
from pydantic import BaseModel, Field
from src.dsl.dslCondition import DslCondition
from src.dsl.mapping import Mapping
from src.dsl.dslForEach import DslForEach

class ConditionPreProcessBlock(BaseModel):
    """Represents a conditional pre-processing block."""
    
    condition: DslCondition = Field(description="Condition for pre-processing")
    preProcessingEntityList: List["PreProcessingEntity"] = Field(description="List of pre-processing entities")

class PreProcessLoop(BaseModel):
    """Represents a pre-processing loop."""
    
    forEach: DslForEach = Field(description="For-each loop configuration")
    preProcessingEntityList: List["PreProcessingEntity"] = Field(description="List of pre-processing entities")

class PreProcessingEntity(BaseModel):
    """Represents a pre-processing entity."""
    
    mapping: Optional[Mapping] = Field(default=None, description="Mapping to apply")
    conditionPreProcessBlockList: Optional[List[ConditionPreProcessBlock]] = Field(default=None, description="List of conditional pre-processing blocks")
    preProcessLoop: Optional[PreProcessLoop] = Field(default=None, description="Pre-processing loop") 