import streamlit as st
from components import LoginDialogComponent, SidebarComponent
from shared import ComponentIDs
from ststeroids import Layout, Store


class LoginLayout(Layout):
    def __init__(
        self,
        session_store: Store,
        login_header: str,
    ):
        self.session_store = session_store
        self.login_header = login_header
        self.sidebar = SidebarComponent.create(ComponentIDs.sidebar)
        self.login_dialog = LoginDialogComponent.create(
            ComponentIDs.dialog_login, self.login_header
        )

    def render(self):
        self.sidebar.render()
        if not self.session_store.has_property("access_token"):
            self.login_dialog.show()
        self.login_dialog.render()
        st.write("Not logged in. Please refresh or use the menu on the left.")
