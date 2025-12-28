import streamlit as st
from ststeroids import Component, Flow


class LoginDialogComponent(Component):
    def __init__(
        self,
        login_flow: Flow,
        # login_success_flow: Flow,
        header: str = "Enter username/password",
    ):
        self.header = header
        self.login_flow = login_flow
        # self.login_success_flow = login_success_flow
        self.visible = False
        self.error_message = None

    def display(self):
        if self.visible:
            print(self.visible)
            self.username = st.text_input("Username")
            self.password = st.text_input("Password", type="password")
            if st.button("Login", use_container_width=True):
                self.login_flow.dispatch()
            if self.error_message:
                st.error(self.error_message)
    def show(self):
        # if self.visible is False:
            self.visible = True
            # st.rerun()

    def hide(self):
        print("hide")
        # if self.visible is True:
        self.visible = False
            # st.rerun()

    def set_error(self, message: str):
        self.error_message = message

    # def clear_error9


