from .route import Route
from .flow_context import FlowContext


class Router:
    """
    Central routing system responsible for selecting and rendering layouts.

    The Router maintains a set of registered routes, determines which route
    is currently active, optionally dispatches route lifecycle flows, and
    renders the corresponding layout.
    """

    def __init__(self, default: str = "__default__"):
        """
        Initialize the Router.

        :param default: The name of the default route to use when no explicit
                        route has been selected.
        """
        self._routes: dict[str, Route] = {}
        self._current: str | None = None
        self._default: str = default

    def register_routes(self, routes: dict[str, Route]) -> None:
        """
        Register the available routes.

        This replaces any previously registered routes.

        :param routes: A mapping of route names to Route instances.
        :return: None
        """
        self._routes = routes

    def route(self, route_name: str) -> None:
        """
        Set the current route to navigate to.

        The route will be resolved and rendered on the next call to `run()`.

        :param route_name: The name of the route to activate.
        :return: None
        """
        self._current = route_name

    def run(self) -> None:
        """
        Resolve and render the active route.

        The router selects the current route if set, otherwise falls back
        to the default route. If the route defines an `on_enter` flow, it
        will be dispatched before rendering the target layout.

        :raises RuntimeError: If no valid route can be resolved.
        :return: None
        """
        if self._current in self._routes:
            route = self._routes[self._current]
        elif self._default in self._routes:
            route = self._routes[self._default]
        else:
            raise RuntimeError(
                "No current route selected and no default route registered."
            )

        if route.on_enter:
            route.on_enter.dispatch(FlowContext("route", route.name))

        route.target.render()
