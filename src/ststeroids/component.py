from typing import Literal, Any
from abc import ABC, abstractmethod
import streamlit as st
from .store import ComponentStore
from .flow import Flow
from .flow_context import FlowContext


# pylint: disable=too-few-public-methods
class Component(ABC):
    """
    Base class for a component that interacts with the the store.

    Attributes:
        id (str): The unique identifier for the component.
        visible (bool) Controls if the component is visible or not.
    """

    id: str
    _events: dict[str, Flow]

    @classmethod
    def create(cls, component_id: str, *args, **kwargs):
        """
        Create a new component instance or return it from the store.

        :param component_id: A unique identifier for the instance of the component

        """
        cls._store = ComponentStore.create("components")

        if cls._store.has_property(component_id):
            return cls._store.get_component(component_id)
        try:
            instance = cls(*args, **kwargs)
            instance.id = component_id
            if not hasattr(instance, "visible"):
                instance.visible = True
            instance._events = {}

            cls._store.init_component(instance)
            return instance
        except TypeError as e:
            raise TypeError(
                f"{str(e)}. This usually happens when you are trying to get a component without creating it first."
            )

    @classmethod
    def get(cls, component_id: str):
        """
        Alias for create() — note that create has to be called first.

        :param component_id: The unique identifier for the instance of the component to return.
        """

        return cls.create(component_id)

    def register_element(self, element_name: str) -> str:
        """
        Generates a unique key for an element based on the instance ID.

        param: element_name: The name of the element to register.

        return: A unique key for the element.
        """
        key = f"{self.id}_{element_name}"
        return key

    def get_element(self, element_name: str) -> Any:
        """
        Retrieves the value of a registered element from the session state.

        param: element_name: The name of the element to retrieve.
        return: The value of the element if it exists in the session state, otherwise None.
        """
        key = f"{self.id}_{element_name}"
        if key not in st.session_state:
            return None
        return st.session_state[key]

    def set_element(self, element_name: str, element_value) -> None:
        """
        Sets the value of a registered element in the session state.

        param: element_name: The name of the element to set.
        param: element_value: The value to assign to the element.
        return: None
        """
        key = f"{self.id}_{element_name}"

        st.session_state[key] = element_value

    def on(self, event_name: str, callback: Flow) -> None:
        """
        Register a Flow callback for a named event on this component.

        :param event_name: The unique name of the event to bind the callback to.
                        Should ideally be a class-level constant to enable autocomplete.
        :param callback: The Flow instance to execute when this event is triggered.
        :return: None
        """
        self._events[event_name] = callback

    def trigger(self, event_name: str) -> None:
        """
        Trigger a previously registered event callback.

        :param event_name: The name of the event to trigger.
        :raises RuntimeError: If no callback has been registered for this event.
        :return: None
        """
        callback = self._events.get(event_name, None)
        if not callback:
            raise RuntimeError(f"{event_name} has not been registered for component with id {self.id}")
        callback.dispatch(FlowContext("component", self.id))

    def render(
        self,
    ) -> None:
        """
        Executes the render method implemented in the subclasses, additionaly providing extra configuration based on the `render_as` parameter
        """

        if not self.visible:
            return
        self.display()

    def show(self):
        self.visible = True

    def hide(self):
        self.visible = False

    @abstractmethod
    def display(self) -> None:
        """
        Abstract method for displaying the component.

        This method should be implemented by subclasses to define how the component is rendered.
        """
        pass
