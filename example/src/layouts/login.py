import streamlit as st
from components import LoginDialogComponent
from shared import ComponentIDs
from ststeroids import Flow, Layout


class LoginLayout(Layout):
    def __init__(
        self,
        login_header: str,
        login_flow: Flow,
        login_success_flow: Flow,
    ):
        self.login_header = login_header
        self.login_dialog = LoginDialogComponent(
            ComponentIDs.dialog_login, login_flow, login_success_flow
        )

    def render(self):
        self.login_dialog.execute_render("dialog", {"title": self.login_header})
        st.write("Not logged in. Please refresh or use the menu on the left.")
        self.login_dialog.show()
