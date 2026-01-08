from dataclasses import dataclass

@dataclass
class FlowContext:
    """
    Encapsulates the context of why a flow is being executed.
    
    Attributes:
        type: The type of the trigger ("component", "route", "app").
        identifier: Optional identifier, e.g., component id, route name.
    """
    type: str
    identifier: str = None