import pytest
import streamlit as st
from unittest.mock import MagicMock
from ststeroids import Router  # Replace 'your_module' with the actual module name

@pytest.fixture
def router():
    return Router()

@pytest.fixture
def mock_session_state(mocker):
    mocker.patch.object(st, "session_state", {}, create=True)


def test_router_initialization(mock_session_state, router):
    assert "ststeroids_current_route" in st.session_state
    assert st.session_state["ststeroids_current_route"] == "home"


def test_router_initialization_with_custom_default(mock_session_state):
    custom_router = Router(default="dashboard")
    assert st.session_state["ststeroids_current_route"] == "dashboard"


def test_register_routes(mock_session_state, router):
    mock_layout = MagicMock()
    routes = {"home": mock_layout, "dashboard": mock_layout}
    router.register_routes(routes)
    assert router.routes == routes


def test_route_changes_current_route(mock_session_state, router):
    router.route("dashboard")
    assert st.session_state["ststeroids_current_route"] == "dashboard"


def test_run_calls_current_route(mock_session_state, router):
    mock_function = MagicMock()
    router.register_routes({"home": mock_function})
    router.run()
    mock_function.assert_called_once()


def test_get_current_route(mock_session_state, router):
    assert router.get_current_route() == "home"
    router.route("dashboard")
    assert router.get_current_route() == "dashboard"
