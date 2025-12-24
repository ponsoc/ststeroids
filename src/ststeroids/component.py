from typing import Literal
from abc import ABC, abstractmethod
import streamlit as st
from .store import ComponentStore
from .flow import Flow


# pylint: disable=too-few-public-methods
class Component(ABC):
    """
    Base class for a component that interacts with the the store.

    Attributes:
        id (str): The unique identifier for the component.
    """

    @classmethod
    def create(cls, component_id: str, *args, **kwargs):
        """
        Create a new component instance or return it from the store.
        """
        cls._store = ComponentStore()

        if cls._store.has_property(component_id):
            return cls._store.get_component(component_id)
        try:
            instance = cls(*args, **kwargs)
            instance.id = component_id
            cls._store.init_component(instance)
            return instance
        except TypeError as e:
            raise TypeError(
                f"{str(e)}. This usually happens when you are trying to get a component without creating it first."
            )

    @classmethod
    def get(cls, component_id: str):
        """
        Alias for create() — creation is implicit.
        """
        return cls.create(component_id)

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

    def _render_dialog(self, title: str):
        """
        Internal method for rendering the component as a dialog.

        This wraps the component's core render logic in a Streamlit dialog with the given title.

        :param title: The title to display at the top of the dialog.
        """

        @st.dialog(title)
        def _render():
            self.render()

        _render()

    def _render_fragment(self, refresh_interval: str = None, refresh_flow: Flow = None):
        """
        Internal method for rendering the component as a fragment.

        This sets up a Streamlit fragment that automatically re-runs at the given interval.
        It internally calls the __render_fragment method.

        This method is not meant to be overridden. Subclasses should implement the render()
        method to define the rendering behavior.

        :param refresh_interval: The interval at which the fragment should refresh (e.g., "5s").
        :param refresh_flow: Optional flow object to pass into the rendering logic.
        """

        @st.fragment(run_every=refresh_interval)
        def _render():
            self.__render_fragment(refresh_flow)

        _render()

    def __render_fragment(self, refresh_flow: Flow = None):
        self.render()
        if refresh_flow:
            refresh_flow.execute_run()

    def execute_render(
        self,
        render_as: Literal["normal", "dialog", "fragment"] = "normal",
        options: dict = {},
    ):
        """
        Executes the render method implemented in the subclasses, additionaly providing extra configuration based on the `render_as` parameter
        """
        match render_as:
            case "normal":
                return self.render()
            case "dialog":
                return self._render_dialog(**options)
            case "fragment":
                return self._render_fragment(**options)
        raise ValueError(f"Unexpected render_as value: {render_as}")

    @abstractmethod
    def render(self) -> None:
        """
        Abstract method for rendering the component.

        This method should be implemented by subclasses to define how the component is rendered.
        """
        pass
