import streamlit as st
from .route import Route


class Router:
    """
    A routing system for the framework, allowing navigation between different layouts.
    """

    def __init__(self, default: str = "__default__"):
        """
        Initializes the Router instance with a default layout.

        :param default: The default route to use when no current route is selected.
        """
        self._routes: dict[str, Route] = {}
        self._current: str | None = None
        self._default: str = default

    def register_routes(self, routes: dict[str, Route]):
        """
        Registers a dictionary of routes where keys are route names and values are layout callables.
        """
        self._routes = routes

    def route(self, route_name: str):
        """
        Sets the current route to execute.

        :param route_name: The name of the route to navigate to.
        """
        self._current = route_name

    def current_route(self) -> str | None:
        """
        Returns the name of the currently selected layout.
        """
        return self._current

    def run(self):
        """
        Executes the callable associated with the current layout.
        Falls back to the default route if none is selected.
        """
        if self._current in self._routes:
            route = self._routes[self._current]
        elif self._default in self._routes:
            route = self._routes[self._default]
        else:
            raise RuntimeError(
                "No current route selected and no default route registered."
            )
        route.target()