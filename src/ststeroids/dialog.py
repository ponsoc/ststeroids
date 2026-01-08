import streamlit as st
from .component import Component

class Dialog(Component):
    """
    Base class for dialog components.

    Dialog components wrap their content inside a Streamlit dialog and provide
    a dedicated method for rendering as a dialog.
    """

    @classmethod
    def create(cls, component_id: str, title: str = "title", *args, **kwargs):
        """
        Create a new Dialog instance or return it from the store.

        :param component_id: Unique identifier for this dialog component.
        :param title: Dialog title.
        :return: Dialog instance
        """
        instance = super().create(component_id, *args, **kwargs)
        instance.title = title
        return instance

    def render(self):
        """
        Renders the component inside a Streamlit dialog context.
        Calls the `display` method to render the contents.
        """
        if not self.visible:
            return
        
        @st.dialog(self.title)
        def _dialog():
            self.display()

        _dialog()