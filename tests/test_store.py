import pytest
from unittest.mock import patch

from ststeroids import Store
from ststeroids.store import ComponentStore


@pytest.fixture
def mock_session_state():
    # Patch Streamlit session_state and return the dict for inspection
    with patch("streamlit.session_state", new={}) as state:
        yield state


# =========================
# Store tests
# =========================


def test_store_initialization(mock_session_state):
    store = Store.create("test_store")

    assert "test_store" in mock_session_state
    assert mock_session_state["test_store"] == {}
    assert store.name == "test_store"


def test_store_set_property(mock_session_state):
    store = Store.create("test_store")
    store.set_property("key", "value")

    assert mock_session_state["test_store"]["key"] == "value"


def test_store_get_property(mock_session_state):
    store = Store.create("test_store")
    store.set_property("key", "value")

    assert store.get_property("key") == "value"


def test_store_del_property(mock_session_state):
    store = Store.create("test_store")
    store.set_property("key", "value")
    store.del_property("key")

    with pytest.raises(KeyError, match="'key' doesn't exist in store 'test_store'."):
        store.get_property("key")


def test_store_get_property_key_error(mock_session_state):
    store = Store.create("test_store")

    with pytest.raises(
        KeyError, match="'missing_key' doesn't exist in store 'test_store'."
    ):
        store.get_property("missing_key")


def test_store_has_property(mock_session_state):
    store = Store.create("test_store")
    store.set_property("key", "value")

    assert store.has_property("key") is True
    assert store.has_property("missing_key") is False


# =========================
# ComponentStore tests
# =========================


def test_component_store_initialization(mock_session_state):
    component_store = ComponentStore.create("components")

    assert "components" in mock_session_state
    assert mock_session_state["components"] == {}
    assert component_store.name == "components"


def test_component_store_init_component(mock_session_state):
    class MockComponent:
        id = "comp1"

    component_store = ComponentStore.create("components")
    component = MockComponent()

    component_store.init_component(component)

    assert component_store.get_component("comp1") is component


def test_component_store_does_not_override_existing_component(mock_session_state):
    class MockComponent:
        id = "comp1"

    component_store = ComponentStore.create("components")

    first = MockComponent()
    second = MockComponent()

    component_store.init_component(first)
    component_store.init_component(second)

    # Should keep the first component
    assert component_store.get_component("comp1") is first


def test_component_store_get_missing_component_raises(mock_session_state):
    component_store = ComponentStore.create("components")

    with pytest.raises(
        KeyError, match="'missing' doesn't exist in store 'components'."
    ):
        component_store.get_component("missing")
