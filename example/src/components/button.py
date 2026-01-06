import streamlit as st
from ststeroids import Component


class ButtonComponent(Component):
    def __init__(self, button_text: str):
        self.button_text = button_text

    def _handle_click(self):
        self.trigger("button_click")

    def display(self):
        st.button(self.button_text, on_click=self._handle_click)
