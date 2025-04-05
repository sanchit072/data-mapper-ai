from typing import Optional
from pydantic import BaseModel, Field
from src.dsl.dslValue import DslValue

class DslTranslation(BaseModel):
    """Represents a translation table mapping."""
    
    tableName: str = Field(description="Name of the translation table")
    value: DslValue = Field(description="Value to be translated")
    defaultValue: Optional[DslValue] = Field(default=None, description="Default value if translation fails") 