import streamlit as st
from ststeroids import Component


class ToastComponent(Component):
    def __init__(
        self,
    ):
        self.visible = False
        self.message = None

    def render(self):
        if self.visible:
            st.toast(self.message)
            self.visible = False

    def set_message(self, message: str):
        print("set called")
        self.message = message
        self.visible = True