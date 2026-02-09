import pytest
from unittest.mock import MagicMock, patch
import streamlit as st

from ststeroids.component import Component
from ststeroids.flow import Flow
from ststeroids.store import ComponentStore
from ststeroids.flow_context import FlowContext


@pytest.fixture
def mock_session_state():
    with patch("streamlit.session_state", new={}) as state:
        yield state


@pytest.fixture
def mock_store():
    store = MagicMock(spec=ComponentStore)
    store.has_property.return_value = False
    return store


@pytest.fixture
def component(mock_store):
    with patch("ststeroids.store.ComponentStore.create", return_value=mock_store):

        class MyComponent(Component):
            def display(self):
                pass

        return MyComponent.create("test_component")


def test_component_create_returns_same_instance(mock_store):
    with patch("ststeroids.store.ComponentStore.create", return_value=mock_store):

        class MyComponent(Component):
            def display(self):
                pass

        comp1 = MyComponent.create("comp")
        comp2 = MyComponent.create("comp")
        # Same store call, simulating singleton
        mock_store.has_property.return_value = True
        mock_store.get_component.return_value = comp1
        comp3 = MyComponent.create("comp")
        assert comp1 is comp3


def test_component_attributes(component):
    assert component.id == "test_component"
    assert hasattr(component, "_events")
    assert component.visible is True


def test_register_element_returns_key(component):
    key = component.register_element("button")
    assert key == "test_component_button"


def test_get_element_and_set_element(mock_session_state, component):
    key = component.register_element("input")
    # Initially None
    assert component.get_element("input") is None
    component.set_element("input", "value")
    assert mock_session_state[key] == "value"
    assert component.get_element("input") == "value"


def test_on_and_trigger_calls_flow(component):
    flow = MagicMock(spec=Flow)
    component.on("click", flow)
    component.trigger("click")
    flow.dispatch.assert_called_once()
    args, _ = flow.dispatch.call_args
    ctx = args[0]
    assert isinstance(ctx, FlowContext)
    assert ctx.identifier == component.id
    assert ctx.type == "component"


def test_trigger_raises_if_event_not_registered(component):
    with pytest.raises(RuntimeError, match="has not been registered"):
        component.trigger("non_existent")


def test_render_calls_display(component):
    component.display = MagicMock()
    component.render()
    component.display.assert_called_once()


def test_render_skips_if_not_visible(component):
    component.display = MagicMock()
    component.hide()
    component.render()
    component.display.assert_not_called()


def test_show_and_hide(component):
    component.hide()
    assert component.visible is False
    component.show()
    assert component.visible is True
