from typing import Any
import streamlit as st
from .store import ComponentStore
from .flow import Flow


# pylint: disable=too-few-public-methods
class Component:
    """
    Base class for a component that interacts with the state and the store.

    Attributes:
        id (str): The unique identifier for the component.
        state (State): The state associated with the component.
    """

    def __init__(self, component_id: str, initial_state: dict = None):
        """
        Initializes the component with a unique ID and initial state.

        :param component_id: The unique identifier for the component.
        :param initial_state: Initial state for the component. Defaults to an empty dictionary.
        """
        self.__store = ComponentStore()
        self.id = component_id
        self.state = State(
            self.id, self.__store, initial_state if initial_state else {}
        )
        self.__store.init_component(self)

    def register_element(self, element_name: str):
        """
        Generates a unique key for an element based on the instance ID.

        Args:
            element_name (str): The name of the element to register.

        Returns:
            str: A unique key for the element.
        """
        key = f"{self.id}_{element_name}"
        return key

    def get_element(self, element_name: str):
        """
        Retrieves the value of a registered element from the session state.

        Args:
            element_name (str): The name of the element to retrieve.

        Returns:
            Any: The value of the element if it exists in the session state, otherwise None.
        """
        key = f"{self.id}_{element_name}"
        if key not in st.session_state:
            return None
        return st.session_state[key]

    def set_element(self, element_name: str, element_value):
        """
        Sets the value of a registered element in the session state.

        Args:
            element_name (str): The name of the element to set.
            element_value (Any): The value to assign to the element.

        Returns:
            None
        """
        key = f"{self.id}_{element_name}"

        st.session_state[key] = element_value

    def render(self) -> None:
        """
        Placeholder method for rendering the component.

        This method should be implemented by subclasses to define how the component is rendered.

        :raises NotImplementedError: If called directly without being implemented in a subclass.
        """
        raise NotImplementedError("Subclasses should implement this method.")

    def _render_fragement(self, refresh_flow: Flow = None):
        if refresh_flow:
            refresh_flow.run()
        self.render()

    def render_as_fragement(
        self, refresh_interval: str = "5s", refresh_flow: Flow = None
    ):
        @st.fragment(run_every=refresh_interval)
        def _render():
            self._render_fragement(refresh_flow)

        _render()


class State:
    """
    Manages the state of a component, storing and retrieving properties
    through the associated store.

    Attributes:
        __id (str): The unique identifier for the component.
        __store (ComponentStore): The store instance that holds the component's state.
    """

    def __init__(self, component_id: str, store: ComponentStore, initial_state: dict):
        """
        Initializes the state for a component, setting up the store and component ID.

        :param component_id: The unique identifier for the component.
        :param store: The store instance where the state is stored.
        :param initial_state: Initial state data for the component.
        """
        super().__setattr__(
            "_State__id", component_id
        )  # Directly set private attributes
        super().__setattr__("_State__store", store)  # Avoid recursion
        store.init_component_state(component_id, initial_state)

    def __getattr__(self, name) -> Any:
        """
        Retrieves a property of the component from the store.

        :param name: The name of the property to retrieve.
        :return: The value of the property from the store.

        :raises AttributeError: If the requested property is not found.
        """
        if not name.startswith("__"):
            return self.__store.get_property(self.__id, name)

    def __setattr__(self, name, value):
        """
        Sets a property of the component in the store.

        :param name: The name of the property to set.
        :param value: The value to set for the property.

        This method avoids recursion for special attributes and handles normal properties.
        """
        if not name.startswith("__"):
            self.__store.set_property(self.__id, name, value)
        else:
            super().__setattr__(name, value)  # Avoid recursion for special attributes
