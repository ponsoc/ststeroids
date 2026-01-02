from .layout import Layout

class Route:
    """
    Represents a single route in the application.

    A route defines:
    - a name (unique identifier),
    - a target (the layout or callable to navigate to),
    - an optional condition that determines if the route is active.

    Attributes:
        name (str): Unique name of the route.
        target (layout): The target layout or callable to execute.
        condition (callable, optional): If provided, the route is active only when this callable returns True.
    """

    def __init__(self, name: str, target: Layout , condition: callable = None):
        """
        Initializes a Route instance.

        :param name: Unique name of the route.
        :param target: Layout to execute when the route is triggered.
        :param condition: Optional callable returning a boolean. If provided, determines if the route is active.
        """
        self.name = name
        self.target = target
        self.condition = condition 