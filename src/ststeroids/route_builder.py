from .layout import Layout
from .route import Route
from .flow import Flow


class RouteBuilder:
    """
    A builder class for defining and registering routes in the application.

    Allows chaining of target and condition definitions before registering the route.

    Example usage:
        RouteBuilder(app, "home").to(HomeLayout).when(user_is_logged_in).register()
    """

    def __init__(self, app, name: str):
        """
        Initializes the RouteBuilder.

        :param app: The application instance where the route will be registered.
        :param name: Unique name of the route.
        """
        self.app = app
        self._name = name
        self._target = None
        self._condition = None
        self._on_enter = None

    def to(self, target: Layout) -> "RouteBuilder":
        """
        Sets the target for this route.

        :param target: Layout class or callable to execute when the route is triggered.
        :return: Self, to allow method chaining.
        """
        self._target = target
        return self

    def when(self, condition: callable) -> "RouteBuilder":
        """
        Sets a condition for this route.

        The route will only be active if the condition evaluates to True.

        :param condition: Callable returning a boolean.
        :return: Self, to allow method chaining.
        """
        self._condition = condition
        return self

    def on_enter(self, callback: Flow):
        self._on_enter = callback
        return self

    def register(self) -> None:
        """
        Registers the route in the application with the specified target and condition.

        Raises:
            ValueError: If no target has been set for the route.
        """
        if self._target is None:
            raise ValueError(
                f"Route '{self._name}' cannot be registered without a target."
            )
        self.app.register(
            Route(self._name, self._target, self._on_enter, self._condition)
        )
