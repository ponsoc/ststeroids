import pytest
from unittest.mock import MagicMock

from ststeroids.router import Router
from ststeroids.route import Route
from ststeroids.flow_context import FlowContext


@pytest.fixture
def router():
    return Router()


def make_route(name="home", on_enter=None):
    target = MagicMock()
    target.render = MagicMock()
    return Route(
        name=name,
        target=target,
        on_enter=on_enter,
    )


def test_router_initialization(router):
    assert router._current is None
    assert router._default == "__default__"
    assert router._routes == {}


def test_router_initialization_with_custom_default():
    router = Router(default="dashboard")
    assert router._default == "dashboard"


def test_register_routes(router):
    route = make_route("home")
    routes = {"home": route}

    router.register_routes(routes)

    assert router._routes == routes


def test_route_sets_current_route(router):
    router.route("dashboard")
    assert router._current == "dashboard"


def test_run_calls_current_route(router):
    route = make_route("home")

    router.register_routes({"home": route})
    router.route("home")
    router.run()

    route.target.render.assert_called_once()


def test_run_calls_on_enter_if_present(router):
    on_enter = MagicMock()
    on_enter.dispatch = MagicMock()

    route = make_route("home", on_enter=on_enter)

    router.register_routes({"home": route})
    router.route("home")
    router.run()

    on_enter.dispatch.assert_called_once()
    args, kwargs = on_enter.dispatch.call_args
    flow_context = args[0]
    assert isinstance(flow_context, FlowContext)
    assert flow_context.identifier == "home"
    assert flow_context.type == "route"

    route.target.render.assert_called_once()


def test_run_falls_back_to_default_route(router):
    default_route = make_route("__default__")

    router.register_routes({"__default__": default_route})
    router.run()

    default_route.target.render.assert_called_once()


def test_run_raises_if_no_current_and_no_default(router):
    router.register_routes({})

    with pytest.raises(
        RuntimeError,
        match="No current route selected and no default route registered.",
    ):
        router.run()


def test_run_uses_default_when_current_is_invalid(router):
    default_route = make_route("__default__")

    router.register_routes({"__default__": default_route})
    router.route("invalid")
    router.run()

    default_route.target.render.assert_called_once()