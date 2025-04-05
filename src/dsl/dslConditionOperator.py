from enum import Enum

class DslConditionOperator(str, Enum):
    """Represents the operators available for conditions."""
    
    EQ = "EQ"  # Equal to
    NE = "NE"  # Not equal to
    GT = "GT"  # Greater than
    LT = "LT"  # Less than
    GE = "GE"  # Greater than or equal to
    LE = "LE"  # Less than or equal to
    HAS_CONTENT = "HAS_CONTENT"  # Has content
    EXISTS = "EXISTS"  # Exists
    CONTAINS = "CONTAINS"  # Contains
    OR = "OR"  # Logical OR
    AND = "AND"  # Logical AND
