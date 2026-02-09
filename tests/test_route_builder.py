import pytest
from unittest.mock import MagicMock

from ststeroids.route_builder import RouteBuilder
from ststeroids.route import Route
from ststeroids.layout import Layout
from ststeroids.flow import Flow


def test_to_when_on_enter_chain_returns_self():
    app = MagicMock()
    builder = RouteBuilder(app, "home")

    class DummyLayout(Layout):
        def render(self):
            pass

    flow = MagicMock(spec=Flow)
    condition = lambda: True

    # Each method should return self for chaining
    assert builder.to(DummyLayout) is builder
    assert builder.when(condition) is builder
    assert builder.on_enter(flow) is builder


def test_register_without_target_raises():
    app = MagicMock()
    builder = RouteBuilder(app, "home")

    with pytest.raises(ValueError, match="cannot be registered without a target"):
        builder.register()


def test_register_calls_app_register_with_route():
    app = MagicMock()
    builder = RouteBuilder(app, "home")

    class DummyLayout(Layout):
        def render(self):
            pass

    flow = MagicMock(spec=Flow)
    condition = lambda: True

    builder.to(DummyLayout).when(condition).on_enter(flow).register()

    # Ensure app.register was called once with a Route instance
    assert app.register.call_count == 1
    route_arg = app.register.call_args[0][0]
    assert isinstance(route_arg, Route)
    assert route_arg.name == "home"
    assert route_arg.target == DummyLayout
    assert route_arg.on_enter == flow
    assert route_arg.condition == condition