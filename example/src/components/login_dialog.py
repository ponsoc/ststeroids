import streamlit as st
from ststeroids import Component


class LoginDialogComponent(Component):
    def __init__(
        self,
        header: str = "Enter username/password",
    ):
        self.header = header
        self.error_message = None
        self.hide()

    def display(self):
        self.username = st.text_input("Username")
        self.password = st.text_input("Password", type="password")
        if st.button("Login", use_container_width=True):
            self.trigger("login_click")
        if self.error_message:
            st.error(self.error_message)
            self.error_message = None

    def set_error(self, message: str):
        self.error_message = message
