import streamlit as st
from ststeroids import Component, Flow


class LoginDialogComponent(Component):
    def __init__(
        self,
        login_flow: Flow,
        header: str = "Enter username/password",
    ):
        self.header = header
        self.login_flow = login_flow
        self.error_message = None
        self.hide()

    def display(self):
        self.username = st.text_input("Username")
        self.password = st.text_input("Password", type="password")
        if st.button("Login", use_container_width=True):
            self.login_flow.dispatch() # via on click, doe hij dan wel een rerun/
        if self.error_message:
            st.error(self.error_message)
            self.error_message = None

    def set_error(self, message: str):
        self.error_message = message
