from ststeroids.route import Route
from ststeroids.layout import Layout
from ststeroids.flow import Flow
from unittest.mock import MagicMock


def test_route_initialization_defaults():
    layout = MagicMock(spec=Layout)
    route = Route(name="home", target=layout)

    assert route.name == "home"
    assert route.target == layout
    assert route.on_enter is None
    assert route.condition is None


def test_route_initialization_with_all_arguments():
    layout = MagicMock(spec=Layout)
    flow = MagicMock(spec=Flow)
    condition = lambda: True

    route = Route(name="dashboard", target=layout, on_enter=flow, condition=condition)

    assert route.name == "dashboard"
    assert route.target == layout
    assert route.on_enter == flow
    assert route.condition == condition
