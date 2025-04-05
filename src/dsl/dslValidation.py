from typing import Optional
from pydantic import BaseModel, Field
from src.dsl.dslCondition import DslCondition

class DslThrowException(BaseModel):
    """Represents an exception to be thrown during validation."""
    
    errorCode: str = Field(description="Error code for the exception")
    errorMessage: str = Field(description="Error message for the exception")
    errorTag: str = Field(description="Error tag for the exception")

class DslSkipInteraction(BaseModel):
    """Represents skipping an interaction during validation."""
    
    targetInteractionNumber: int = Field(description="Interaction number to skip")

class DslValidationAction(BaseModel):
    """Represents an action to take during validation."""
    
    throwException: Optional[DslThrowException] = Field(default=None, description="Exception to throw")
    skipInteraction: Optional[DslSkipInteraction] = Field(default=None, description="Interaction to skip")

class DslValidation(BaseModel):
    """Represents a validation rule in the DSL."""
    
    condition: DslCondition = Field(description="Condition to validate")
    action: DslValidationAction = Field(description="Action to take if validation fails") 