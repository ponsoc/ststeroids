import pytest
from unittest.mock import patch
from ststeroids import Store
from ststeroids.store import ComponentStore


@pytest.fixture
def mock_session_state():
    with patch("streamlit.session_state", new={}) as mock_state:
        yield mock_state


def test_store_initialization(mock_session_state):
    store = Store("test_store")
    assert "test_store" in mock_session_state
    assert mock_session_state["test_store"] == {}


def test_store_set_property(mock_session_state):
    store = Store("test_store")
    store.set_property("key", "value")
    assert mock_session_state["test_store"]["key"] == "value"


def test_store_get_property(mock_session_state):
    store = Store("test_store")
    store.set_property("key", "value")
    assert store.get_property("key") == "value"


def test_store_get_property_key_error(mock_session_state):
    store = Store("test_store")
    with pytest.raises(
        KeyError, match="'missing_key' doesn't exist in store 'test_store'."
    ):
        store.get_property("missing_key")


def test_store_has_property(mock_session_state):
    store = Store("test_store")
    store.set_property("key", "value")
    assert store.has_property("key") is True
    assert store.has_property("missing_key") is False


def test_component_store_initialization(mock_session_state):
    component_store = ComponentStore()
    assert "components" in mock_session_state
    assert mock_session_state["components"] == {}


def test_component_store_init_component(mock_session_state):
    class MockComponent:
        id = "comp1"

    component_store = ComponentStore()
    component = MockComponent()
    component_store.init_component(component)
    assert component_store.get_component("comp1") == component


def test_component_store_init_component_state(mock_session_state):
    component_store = ComponentStore()
    component_store.init_component_state("comp1", {"state_key": "state_value"})
    assert component_store.get_property("comp1", "state_key") == "state_value"


def test_component_store_set_get_property(mock_session_state):
    component_store = ComponentStore()
    component_store.init_component_state("comp1", {})
    component_store.set_property("comp1", "prop", "value")
    assert component_store.get_property("comp1", "prop") == "value"
