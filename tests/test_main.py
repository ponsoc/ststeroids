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


# ----------------------------
# Unit tests for helpers
# ----------------------------

def test_get_active_routes_filters_correctly(app):
    class MyLayout(Layout):
        def render(self): pass

    route_true = Route("true_route", MyLayout(), condition=lambda: True)
    route_false = Route("false_route", MyLayout(), condition=lambda: False)
    app.register(route_true)
    app.register(route_false)
    app._default = Route("__default__", MyLayout())

    active_routes = app._get_active_routes()
    assert "true_route" in active_routes
    assert "false_route" not in active_routes
    assert "__default__" in active_routes


def test_trigger_run_once_event_only_runs_once(app, mock_session_state):
    flow = MagicMock(spec=Flow)
    app._on_app_run_once = flow

    # First call triggers dispatch
    app._trigger_run_once_event()
    flow.dispatch.assert_called_once()
    assert mock_session_state["_on_app_run_once_done"] is True

    # Second call does not trigger dispatch
    flow.reset_mock()
    app._trigger_run_once_event()
    flow.dispatch.assert_not_called()


def test_handle_scheduled_rerun_executes_and_reruns(app, mock_session_state):
    fn = MagicMock()
    mock_session_state["_schedule_rerun"] = {"fn": fn, "args": (1,), "kwargs": {"a": 2}}

    # Patch st.rerun to avoid actually rerunning
    with patch("streamlit.rerun") as mock_rerun:
        app._handle_scheduled_rerun()

    fn.assert_called_once_with(1, a=2)
    mock_rerun.assert_called_once()
    assert "_schedule_rerun" not in mock_session_state


# ----------------------------
# Integration tests for run
# ----------------------------

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


def test_run_calls_helpers_and_router_methods(app, mock_session_state):
    flow = MagicMock(spec=Flow)
    app.on_app_run_once(flow)

    route = Route("home", MagicMock())
    app.register(route)

    app._router.register_routes = MagicMock()
    app._router.route = MagicMock()
    app._router.run = MagicMock()

    # Patch the helpers to ensure they are called
    with patch.object(app, "_trigger_run_once_event") as mock_trigger, \
         patch.object(app, "_get_active_routes") as mock_routes, \
         patch.object(app, "_handle_scheduled_rerun") as mock_rerun:

        mock_routes.return_value = {"home": route}

        app.run(entry_route="home")

        mock_trigger.assert_called_once()
        mock_routes.assert_called_once()
        mock_rerun.assert_called_once()
        app._router.register_routes.assert_called_once_with({"home": route})
        app._router.route.assert_called_once_with("home")
        app._router.run.assert_called_once()


def test_run_filters_routes_by_condition(app):
    class MyLayout(Layout):
        def render(self): pass

    route_true = Route("true_route", MyLayout(), condition=lambda: True)
    route_false = Route("false_route", MyLayout(), condition=lambda: False)
    app.register(route_true)
    app.register(route_false)

    app._router.register_routes = MagicMock()
    app._router.route = MagicMock()
    app._router.run = MagicMock()

    app.run()
    routes_passed = app._router.register_routes.call_args[0][0]

    assert "true_route" in routes_passed
    assert "false_route" not in routes_passed


# ----------------------------
# Other basic tests
# ----------------------------

def test_route_returns_routebuilder(app):
    rb = app.route("home")
    from ststeroids.route_builder import RouteBuilder
    assert isinstance(rb, RouteBuilder)


def test_default_route_sets_default(app):
    class MyLayout(Layout):
        def render(self): pass

    layout = MyLayout()
    app.default_route(layout)
    assert app._default.name == "__default__"
    assert app._default.target == layout


def test_register_adds_route(app):
    class MyLayout(Layout):
        def render(self): pass

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