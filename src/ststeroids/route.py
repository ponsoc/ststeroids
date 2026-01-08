from .layout import Layout
from .flow import Flow


class Route:
    """
    Represents a single route in the application.

    A route defines:
    - a name (unique identifier),
    - a target (the layout or callable to navigate to),
    - an optional flow to dispatch when the route is entered,
    - an optional condition that determines if the route is active.

    Attributes:
        name (str): Unique name of the route.
        target (layout): The target layout to render.
        on_enter (flow): The flow to dispatch when the route is entered.
        condition (callable, optional): If provided, the route is active only when this callable returns True.
    """

    def __init__(
        self,
        name: str,
        target: Layout,
        on_enter: Flow = None,
        condition: callable = None,
    ):
        """
        Initializes a Route instance.

        :param name: Unique name of the route.
        :param target: Layout to render when the route is triggered.
        :param on_enter: Flow to dispatch when the route is entered.
        :param condition: Optional callable returning a boolean. If provided, determines if the route is active.
        """
        self.name = name
        self.target = target
        self.on_enter = on_enter
        self.condition = condition
