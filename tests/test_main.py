import pytest
from unittest.mock import MagicMock, patch

from ststeroids import StSteroids
from ststeroids.route import Route
from ststeroids.layout import Layout
from ststeroids.flow import Flow


@pytest.fixture
def mock_session_state():
    # Patch Streamlit session_state and return the dict for inspection
    with patch("streamlit.session_state", new={}) as state:
        yield state


@pytest.fixture
def app():
    return StSteroids()


def test_route_returns_routebuilder(app):
    rb = app.route("home")
    from ststeroids.route_builder import RouteBuilder

    assert isinstance(rb, RouteBuilder)


def test_default_route_sets_default(app):
    class MyLayout(Layout):
        def render(self):
            pass

    layout = MyLayout()
    app.default_route(layout)

    assert app._default.name == "__default__"
    assert app._default.target == layout


def test_register_adds_route(app):
    class MyLayout(Layout):
        def render(self):
            pass

    layout = MyLayout()
    route = Route("home", layout)

    app.register(route)

    assert "home" in app._routes
    assert app._routes["home"] == route


def test_on_app_run_once_registers_flow(app):
    flow = MagicMock(spec=Flow)

    app.on_app_run_once(flow)
    assert app._on_app_run_once == flow

    with pytest.raises(RuntimeError):
        app.on_app_run_once(flow)


def test_run_triggers_on_app_run_once_only_once(app, mock_session_state):
    flow = MagicMock(spec=Flow)
    app.on_app_run_once(flow)

    app._router.register_routes = MagicMock()
    app._router.route = MagicMock()
    app._router.run = MagicMock()

    # First run
    app.run()

    flow.dispatch.assert_called_once()
    assert "_on_app_run_once_done" in mock_session_state
    assert mock_session_state["_on_app_run_once_done"] is True

    # Second run
    flow.reset_mock()
    app.run()

    flow.dispatch.assert_not_called()


def test_run_filters_routes_by_condition(app):
    class MyLayout(Layout):
        def render(self):
            pass

    route_true = Route(
        "true_route",
        MyLayout(),
        condition=lambda: True,
    )

    route_false = Route(
        "false_route",
        MyLayout(),
        condition=lambda: False,
    )

    app.register(route_true)
    app.register(route_false)

    app._router.register_routes = MagicMock()
    app._router.route = MagicMock()
    app._router.run = MagicMock()

    app.run()

    routes_passed = app._router.register_routes.call_args[0][0]

    assert "true_route" in routes_passed
    assert "false_route" not in routes_passed


def test_run_calls_router_methods(app):
    class MyLayout(Layout):
        def render(self):
            pass

    route = Route("home", MyLayout())
    app.register(route)

    app._router.register_routes = MagicMock()
    app._router.route = MagicMock()
    app._router.run = MagicMock()

    app.run(entry_route="home")

    app._router.register_routes.assert_called_once()
    app._router.route.assert_called_once_with("home")
    app._router.run.assert_called_once()