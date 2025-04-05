from typing import List, Optional
from pydantic import BaseModel, Field
from src.dsl.dslConditionalMapping import DslConditionalMapping
from src.dsl.dslValidation import DslValidation
from src.dsl.dslPreProcessing import PreProcessingEntity

# Pydantic
class DslMapping(BaseModel):
    """The parent class for all DSL mappings."""

    format: str = Field(default="JSON", description="Format of the mapping (JSON, XML, STRING)")
    headers: Optional[DslConditionalMapping] = Field(default=None, description="Headers mapping")
    validationList: Optional[List[DslValidation]] = Field(default=None, description="List of validations")
    preProcessList: Optional[List[PreProcessingEntity]] = Field(default=None, description="List of pre-processing entities")
    conditionalMappingList: Optional[List[DslConditionalMapping]] = Field(default=None, description="List of conditional mappings")