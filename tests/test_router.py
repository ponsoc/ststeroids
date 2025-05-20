from collections import defaultdict
import pytest
import streamlit as st
from unittest.mock import MagicMock
from ststeroids import Router


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


def test_run_calls_current_route_that_raises_an_exception(mock_session_state, router):
    mock_function = MagicMock(side_effect=KeyError("Missing key"))
    router.register_routes({"home": mock_function})
    with pytest.raises(KeyError, match="Missing key"):
        router.route("home")
        router.run()


def test_run_calls_invalid_current_route(mock_session_state, router):
    mock_function = MagicMock()
    router.register_routes({"home": mock_function})
    with pytest.raises(
        KeyError, match="The current route 'invalid' is not a registered route."
    ):
        router.route("invalid")
        router.run()


def test_run_calls_with_defaultdict(mock_session_state, router):
    mock_function = MagicMock()
    default_function = MagicMock()

    # Use defaultdict to return default_function for any missing keys
    router.register_routes(
        defaultdict(lambda: default_function, {"home": mock_function})
    )

    router.route(
        "invalid"
    )  # This will now return default_function instead of raising KeyError
    router.run()

    # Ensure the default function is called
    default_function.assert_called_once()
    # Ensure the "home" function is not called
    mock_function.assert_not_called()


def test_get_current_route(mock_session_state, router):
    assert router.get_current_route() == "home"
    router.route("dashboard")
    assert router.get_current_route() == "dashboard"
