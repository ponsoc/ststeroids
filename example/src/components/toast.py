import streamlit as st
from ststeroids import Component


class ToastComponent(Component):
    def __init__(
        self,
    ):
        self.message = None
        self.hide()

    def display(self):
        st.toast(self.message)
        self.hide()

    def set_message(self, message: str):
        self.message = message
        self.show()
