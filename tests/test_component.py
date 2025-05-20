from unittest.mock import MagicMock, patch
import pytest
from ststeroids.store import ComponentStore
from ststeroids.component import Component, State


@pytest.fixture
def mock_session_state():
    with patch("streamlit.session_state", new={}) as mock_state:
        yield mock_state


@pytest.fixture
def mock_store():
    # Mocking the ComponentStore for testing purposes
    store = MagicMock(spec=ComponentStore)
    return store


@pytest.fixture
def component(mock_store):
    # Creating a sample component for testing
    component = Component(component_id="test_component", initial_state={"key": "value"})
    component._Component__store = (
        mock_store  # Injecting the mock store into the component
    )
    return component


def test_component_initialization(component):
    # Test that the component is initialized correctly
    assert component.id == "test_component"
    assert isinstance(component.state, State)


def test_state_initialization(mock_store):
    # Test that the state is initialized with the component ID and store
    state = State(
        component_id="test_component", store=mock_store, initial_state={"key": "value"}
    )
    mock_store.init_component_state.assert_called_once_with(
        "test_component", {"key": "value"}
    )
    assert state._State__id == "test_component"
    assert state._State__store == mock_store


def test_getattr(mock_store, component):
    # Test that attributes are retrieved correctly from the store
    assert component.state.key == "value"


def test_setattr(mock_store, component):
    # Test that attributes are set correctly in the store
    component.state.key = "new_value"
    assert component.state.key == "new_value"


def test_render_not_implemented(component):
    # Test that calling render raises NotImplementedError
    with pytest.raises(NotImplementedError):
        component.render()


def test_register_element(component):
    element_name = "button"
    expected_key = "test_component_button"
    assert component.register_element(element_name) == expected_key


def test_get_element_not_set(component):
    element_name = "non_existent"
    assert component.get_element(element_name) is None


def test_get_element_set(component, mock_session_state):
    element_name = "input"
    key = component.register_element(element_name)
    mock_session_state[key] = "Test Value"
    assert component.get_element(element_name) == "Test Value"


def test_set_element(component, mock_session_state):
    element_name = "input"
    key = component.register_element(element_name)
    mock_session_state[key] = "nothing"
    component.set_element(element_name, "something")
    assert component.get_element(element_name) == "something"


def test_render_fragment_with_flow(component):
    mock_flow = MagicMock()
    component.render = MagicMock()

    component._render_fragement(refresh_flow=mock_flow)

    mock_flow.run.assert_called_once()
    component.render.assert_called_once()
