from unittest.mock import MagicMock, patch
import pytest
from ststeroids.store import ComponentStore
from ststeroids.component import Component, State


@pytest.fixture
def mock_session_state():
    with patch("streamlit.session_state", new={}) as mock_state:
        yield mock_state


@pytest.fixture(scope="session")
def mock_store():
    # Mocking the ComponentStore for testing purposes
    store = MagicMock(spec=ComponentStore)
    return store


@pytest.fixture(scope="session")
def component(mock_store):
    # Creating a sample component for testing
    component = Component(component_id="test_component", initial_state={"key": "value"})
    component._Component__store = (
        mock_store  # Injecting the mock store into the component
    )
    return component

def test_component_creation_without_id():
    with pytest.raises(KeyError):
        component = Component(initial_state={"key": "value"})

def test_component_singleton():
    first_instance = Component(component_id="test_component", initial_state={"key": "value"})
    second_instance = Component(component_id="test_component", initial_state={"key": "value"})
    assert first_instance is second_instance

def test_subclass_init_runs_only_once():
    calls = {"count": 0}

    class Sub(Component):
        def __init__(self, value):
            calls["count"] += 1
            self.value = value

    obj = Sub(42)
    assert obj.value == 42
    assert calls["count"] == 1  # __init__ ran once

    # Call __init__ again explicitly
    obj.__init__(99)
    assert obj.value == 42       # value didn't change
    assert calls["count"] == 1   # __init__ not called again


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


def test_getattr(component):
    # Test that attributes are retrieved correctly from the store
    assert component.state.key == "value"


def test_setattr(component):
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


def test__render_fragment_with_flow(component):
    mock_flow = MagicMock()
    component.render = MagicMock()

    component._Component__render_fragment(refresh_flow=mock_flow)

    mock_flow.execute_run.assert_called_once()
    component.render.assert_called_once()


def test_execute_render_normal(component):
    component.render = MagicMock(return_value="normal_rendered")
    result = component.execute_render(render_as="normal")
    component.render.assert_called_once()
    assert result == "normal_rendered"


def test_execute_render_dialog(component):
    component._render_dialog = MagicMock(return_value="dialog_rendered")
    result = component.execute_render(render_as="dialog", options={"title": "bar"})
    component._render_dialog.assert_called_once_with(title="bar")
    assert result == "dialog_rendered"


def test_execute_render_fragment(component):
    component._render_fragment = MagicMock(return_value="fragment_rendered")
    result = component.execute_render(render_as="fragment", options={"x": 1})
    component._render_fragment.assert_called_once_with(x=1)
    assert result == "fragment_rendered"
