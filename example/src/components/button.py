import streamlit as st
from ststeroids import Component, Flow


class ButtonComponent(Component):

    EVENT_ClICK = "click"

    def __init__(self, button_text: str):
        self.button_text = button_text

    def _handle_click(self):
        self.trigger(self.EVENT_ClICK)

    def display(self):
        st.button(self.button_text, on_click=self._handle_click)

    def on_click(self, flow: Flow) -> None:
        """
        Register a flow to be executed when the user clicks the button.
        """
        self.on(self.EVENT_ClICK, flow)
