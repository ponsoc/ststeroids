import streamlit as st
from ststeroids import Component, Flow


class LoginDialogComponent(Component):

    EVENT_LOGIN = "login"

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
            self.trigger(self.EVENT_LOGIN)
        if self.error_message:
            st.error(self.error_message)
            self.error_message = None

    def on_login(self, flow: Flow) -> None:
        """
        Register a flow to be executed when the user clicks the login button.
        """
        self.on(self.EVENT_LOGIN, flow)

    def set_error(self, message: str):
        self.error_message = message
