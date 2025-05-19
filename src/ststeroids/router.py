import streamlit as st
from .layout import Layout


class Router:
    """
    A routing system for Streamlit applications, allowing navigation between different pages.
    """

    def __init__(self, default: str = "home"):
        """
        Initializes the Router instance with a default page.

        :param default: The default page to load when the app starts. Defaults to "home".
        """
        self.routes = {}
        if "ststeroids_current_route" not in st.session_state:
            st.session_state["ststeroids_current_route"] = default

    def run(self):
        """
        Executes the function associated with the currently active route.

        :return: None
        """
        try:
            route = self.routes[st.session_state["ststeroids_current_route"]]
        except KeyError as exc:
            raise KeyError(
                f"The current route '{st.session_state['ststeroids_current_route']}' is not a registered route."
            ) from exc
        route()

    def route(self, route_name: str):
        """
        Updates the current page in the session state.

        :param route_name: The name of the route to navigate to.
        :return: None
        """
        st.session_state["ststeroids_current_route"] = route_name

    def register_routes(self, routes: dict[str, Layout]):
        """
        Registers a dictionary of routes where keys are route names and values are layouts.

        :param routes: A dictionary mapping route names to layouts.
        :return: None
        """
        self.routes = routes

    def get_current_route(self):
        if "ststeroids_current_route" in st.session_state:
            return st.session_state["ststeroids_current_route"]
        return None
