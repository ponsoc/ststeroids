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
    # component._Component__store = mock_store  # Injecting the mock store into the component
    return component

def test_component_initialization(component):
    # Test that the component is initialized correctly
    assert component.id == "test_component"
    assert component.state is not None
    print("cp state", component.state.store)

def test_state_initialization(mock_store):
    # Test that the state is initialized with the component ID and store
    state = State(component_id="test_component", store=mock_store, initial_state={"key": "value"})
    mock_store.init_component_state.assert_called_once_with("test_component", {"key": "value"})
    assert state._State__id == "test_component"
    assert state._State__store == mock_store

# def test_getattr(mock_store, component):
#     # Test that attributes are retrieved correctly from the store
#     mock_store.get_property.return_value = "value_from_store"
#     test = component.state.key  # Accessing the 'key' attribute
#     # Debugging: print out the calls made to get_property
#     print("Mock calls to get_property:", component.call_args_list)
#     # mock_store.get_property.assert_called_with("test_component", "key")
#     # assert component.state.key == "value_from_store"

# def test_setattr(mock_store, component):
#     # Test that attributes are set correctly in the store
#     component.state.key = "new_value"
#     mock_store.set_property.assert_called_with("test_component", "key", "new_value")

def test_render_not_implemented(component):
    # Test that calling render raises NotImplementedError
    with pytest.raises(NotImplementedError):
        component.render()

# def test_state_getattr_attribute_error(mock_store):
#     # Test that an AttributeError is raised if an invalid attribute is accessed
#     state = State(component_id="test_component", store=mock_store, initial_state={})
#     with pytest.raises(AttributeError):
#         state.invalid_attribute  # Trying to access an invalid attribute

# def test_state_setattr_special_attribute(mock_store):
#     # Test that special attributes are handled correctly in State class
#     state = State(component_id="test_component", store=mock_store, initial_state={})
#     state.__id = "new_id"  # This should not call the store
#     assert state._State__id == "new_id"