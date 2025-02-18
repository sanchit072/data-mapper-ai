from enum import Enum

class DslBase(str, Enum):
    """Represents the base value from which xpath and jsonpath will be taken. For CSV files, this is always INTERACTION_1_RESPONSE_BODY if we are applying carrier mapping. For constant mappings, it is always NO_BASE"""

    INTERACTION_1_RESPONSE_BODY = "INTERACTION_1_RESPONSE_BODY"
    NO_BASE = "NO_BASE"
    
    