import streamlit as st
from ststeroids import Component, Flow


class LoginDialogComponent(Component):
    def __init__(
        self,
        login_flow: Flow,
        login_success_flow: Flow,
        header: str = "Enter username/password",
    ):
        self.header = header
        self.login_flow = login_flow
        self.login_success_flow = login_success_flow
        self.visible = False

    def render(self):
        if self.visible:
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            if st.button("Login", use_container_width=True):
                login_succes = self.login_flow.execute_run(username, password)
                if login_succes:
                    self.login_success_flow.execute_run()
                else:
                    st.error("Login failed, please check your username and password.")

    def show(self):
        if self.visible is False:
            self.visible = True
            st.rerun()

    def hide(self):
        if self.visible is True:
            self.visible = False
            st.rerun()
