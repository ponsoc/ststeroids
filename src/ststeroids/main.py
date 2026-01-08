from .route import Route
from .route_builder import RouteBuilder
from .router import Router
from .layout import Layout
from .flow import Flow
import streamlit as st
from .flow_context import FlowContext


class StSteroids:
    """
    The main application class for managing routes and navigation.

    StSteroids handles registration of routes, setting a default route,
    and running the router to navigate to the appropriate page or layout.
    """

    def __init__(self):
        """
        Initializes the StSteroids application instance.
        """
        self._router = Router()
        self._routes: dict[str, Route] = {}
        self._default: Route | None = None
        self._on_app_run_once = None
        self._on_app_run = None

    def route(self, name: str) -> RouteBuilder:
        """
        Creates a RouteBuilder for defining a new route.

        Example usage:
            app.route("home").to(HomeLayout).when(user_is_logged_in).register()

        :param name: The unique name of the route.
        :return: RouteBuilder instance to define target and condition before registering.
        """
        return RouteBuilder(self, name)

    def default_route(self, target: Layout) -> None:
        """
        Sets the default route for the application.

        The default route is used if no other route is specified when running the app.

        :param target: The target layout for the default route.
        """
        self._default = Route("__default__", target)

    def register(self, route: Route) -> None:
        """
        Registers a route in the application.

        :param route: The Route instance to register.
        """
        self._routes[route.name] = route

    def on_app_run_once(self, callback: Flow) -> None:
        """
        Registers a flow to be executed once when the application starts.

        This flow will be triggered only the first time the app runs.
        Subsequent reruns of the app will not re-execute this flow.

        :param callback: The Flow instance to execute on the first app run.
        :raises RuntimeError: If an on_app_run_once flow has already been registered.
        :return: None
        """
        if self._on_app_run_once:
            raise RuntimeError("on_app_run_once already registered.")
        self._on_app_run_once = callback

    def run(self, entry_route: str | None = None) -> None:
        """
        Runs the application router.

        Filters routes based on their conditions, registers active routes
        with the router, navigates to the specified entry route if provided,
        and starts the router.

        :param entry_route: Optional name of the route to navigate to immediately.
        :return: None
        """
        if "_on_app_run_once_done" not in st.session_state and self._on_app_run_once:
            self._on_app_run_once.dispatch(FlowContext("app","run_once"))
            st.session_state["_on_app_run_once_done"] = True

        routes = {}

        if self._default:
            routes["__default__"] = self._default

        for route in self._routes.values():
            if route.condition:
                if route.condition():
                    routes[route.name] = route
            else:
                routes[route.name] = route

        self._router.register_routes(routes)

        if entry_route:
            self._router.route(entry_route)

        self._router.run()
