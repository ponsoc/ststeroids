import streamlit as st
from .layout import Layout


class Router:
    """
    A routing system for Streamlit applications, handles which layout is rendered.
    """

    routes = {}
    st.session_state["ststeroids_current_route"] = "home"
    
    @staticmethod
    def update_default_route(route_name: str):
        """
        Updates the Router's default route.

        :param route_name: The default route for when the app starts.
        """
        if "ststeroids_current_route" not in st.session_state:
            st.session_state["ststeroids_current_route"] = route_name

    @classmethod
    def run(cls):
        """
        Executes the function associated with the currently active route.

        :return: None
        """
        try:
            route = cls.routes[st.session_state["ststeroids_current_route"]]
        except KeyError as exc:
            raise KeyError(
                f"The current route '{st.session_state['ststeroids_current_route']}' is not a registered route."
            ) from exc
        route()

    @staticmethod
    def route(route_name: str):
        """
        Updates the current route in the session state.

        :param route_name: The name of the route to navigate to.
        :return: None
        """
        st.session_state["ststeroids_current_route"] = route_name

    
    @classmethod
    def register_routes(cls, routes: dict[str, Layout]):
        """
        Registers a dictionary of routes where keys are route names and values are layouts.

        :param routes: A dictionary mapping route names to layouts.
        :return: None
        """
        cls.routes = routes

    @staticmethod
    def get_current_route():
        if "ststeroids_current_route" in st.session_state:
            return st.session_state["ststeroids_current_route"]
        return None
