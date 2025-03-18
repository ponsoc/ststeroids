import pytest
from unittest.mock import MagicMock
from ststeroids.store import ComponentStore
from ststeroids.component import Component, State

@pytest.fixture
def mock_store():
    # Mocking the ComponentStore for testing purposes
    store = MagicMock(spec=ComponentStore)
    return store

@pytest.fixture
def component(mock_store):
    # Creating a sample component for testing
    component = Component(component_id="test_component", initial_state={"key": "value"})
    component._Component__store = mock_store  # Injecting the mock store into the component
    return component

def test_component_initialization(component):
    # Test that the component is initialized correctly
    assert component.id == "test_component"
    assert isinstance(component.state, State)

def test_state_initialization(mock_store):
    # Test that the state is initialized with the component ID and store
    state = State(component_id="test_component", store=mock_store, initial_state={"key": "value"})
    mock_store.init_component_state.assert_called_once_with("test_component", {"key": "value"})
    assert state._State__id == "test_component"
    assert state._State__store == mock_store


def test_render_not_implemented(component):
    # Test that calling render raises NotImplementedError
    with pytest.raises(NotImplementedError):
        component.render()
