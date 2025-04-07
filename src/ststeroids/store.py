from typing import Any
import streamlit as st


class Store:
    """
    Class for creating a session store.

    This class manages storing and retrieving properties in Streamlit's session state.
    It initializes a store with a unique name and allows properties to be set and retrieved.

    :param store_name: The name of the store to create in session state.
    """

    def __init__(self, store_name: str):
        """
        Initializes the session store with the given name.

        :param store_name: The name of the store to create in session state.
        """
        self.name = store_name
        if store_name not in st.session_state:
            st.session_state[self.name] = {}

    def has_property(self, property_name: str) -> bool:
        """
        Checks if a property exists in the store.

        :param property_name: The name of the property to check.
        :return: True if the property exists, False otherwise.
        """
        return property_name in st.session_state.get(self.name, {})

    def get_property(self, property_name: str) -> Any:
        """
        Retrieves the value of a property from the store.

        :param property_name: The name of the property to retrieve.
        :return: The value of the property from the store.
        """
        if property_name not in st.session_state[self.name]:
            raise KeyError(f"'{property_name}' doesn't exist in store '{self.name}'.")
        return st.session_state[self.name][property_name]

    def set_property(self, property_name: str, property_value: Any) -> None:
        """
        Sets the value of a property in the store.

        :param property_name: The name of the property to set.
        :param property_value: The value to set for the property.
        :return: None
        """
        st.session_state[self.name][property_name] = property_value


class ComponentStore(Store):
    """
    Class that creates a component session store. This can be passed to component instances.

    :param component_id: The unique identifier for the component.
    :param initial_state: The initial state of the component.
    """

    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        """
        Initializes the component store with the name 'components'.

        This store is used specifically for storing component-related state in the session.
        """
        super().__init__("components")

    def init_component(self, component: object) -> None:
        """
        Initializes a component in the session store with its ID

        :param component_id: The unique identifier for the component.
        :return: None
        """
        if not self.has_property(component.id):
            super().set_property(component.id, component)

    def init_component_state(self, component_id: str, initial_state: dict) -> None:
        """
        Initializes a component state in the session store with its ID and initial state.

        :param component_id: The unique identifier for the component.
        :param initial_state: The initial state to set for the component.
        :return: None
        """
        if not self.has_property(f"{component_id}_state"):
            super().set_property(f"{component_id}_state", initial_state)

    def get_property(  # pylint: disable=arguments-differ
        self, component_id: str, property_name: str
    ) -> Any:
        """
        Retrieves the value of a property from a component's state.

        :param component_id: The unique identifier for the component.
        :param property_name: The name of the property to retrieve.
        :return: The value of the property from the component's state.
        """
        return super().get_property(f"{component_id}_state")[property_name]

    def set_property(  # pylint: disable=arguments-differ
        self, component_id: str, property_name: str, property_value: Any
    ) -> None:
        """
        Sets the value of a property in a component's state.

        :param component_id: The unique identifier for the component.
        :param property_name: The name of the property to set.
        :param property_value: The value to set for the property.
        :return: None
        """
        component_state = super().get_property(f"{component_id}_state")
        component_state[property_name] = property_value
        super().set_property(f"{component_id}_state", component_state)

    def get_component(self, component_id: str):
        """
        Retrieves the current state or properties of a component.

        :param component_id: The unique identifier for the component.
        :return: The component's state or properties.
        """
        return super().get_property(component_id)
