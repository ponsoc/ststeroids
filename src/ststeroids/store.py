from typing import Any
import streamlit as st


class Store:
    """
    Class for creating a session store.

    This class manages storing and retrieving properties in Streamlit's session state.
    
    Attributes:
            name (str): Unique name of the store.
    """

    def __init__(self, store_name: str):
        """
        Initializes a store with a unique name and allows properties to be set and retrieved. Do not use directly, use create instead.

        :param store_name: The name of the store to create in session state.
        """
        self.name = store_name
        if store_name not in st.session_state:
            st.session_state[store_name] = {}

    @classmethod
    def create(cls, store_name: str):
        """
        Creates a new instance of the store with a unique name and allows properties to be set and retrieved.

        :param store_name: The name of the store to create in session state.
        """
        return cls(store_name)

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

    def del_property(self, property_name: str) -> None:
        """
        Deletes the property in the store.

        :param property_name: The name of the property to delete
        :return: None
        """

        del st.session_state[self.name][property_name]


class ComponentStore(Store):
    """
    Class that creates a component session store.

    """

    def init_component(self, component: object) -> None:
        """
        Initializes a component in the session store with its ID

        :param component: The component instance.
        :return: None
        """
        if not self.has_property(component.id):
            super().set_property(component.id, component)

    def get_component(self, component_id: str):
        """
        Retrieves the current state or properties of a component.

        :param component_id: The unique identifier for the component.
        :return: The component's state or properties.
        """
        return super().get_property(component_id)
