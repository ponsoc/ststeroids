import streamlit as st
from flows import LoginFlow, LoginSuccessFlow, RefreshFlow
from layouts import LoginLayout, DashboardLayout, ManageDataLayout
from service import MockBackendService
from ststeroids import Store, Style, StSteroids



class MainApp:

    def __init__(self):
        self.session_store = Store.create("store")

        self.backend_service = MockBackendService("./example/test_data.json")
        self.login_flow = LoginFlow.create(self.session_store, self.backend_service)
        self.login_success_flow = LoginSuccessFlow.create(
            self.session_store, self.backend_service
        )
        self.refresh_flow = RefreshFlow.create(self.session_store, self.backend_service)

        st.set_page_config(page_title="StSteroids Example app", layout="wide")

        app_style = Style("./example/src/assets/style.css")
        app_style.apply_style()

        self.login_layout = LoginLayout.create(
            self.session_store,
            "App login", self.login_flow, self.login_success_flow
        )
        self.dashboard_layout = DashboardLayout.create(self.refresh_flow)
        self.manage_data_layout = ManageDataLayout.create()

        self.app = StSteroids()

        self.app.default_route(self.login_layout)

        self.app.route("login").to(self.login_layout).register()
        self.app.route("dashboard").to(self.dashboard_layout).when(
            lambda: self.session_store.has_property("access_token")
        ).register()
        self.app.route("manage_data").to(self.manage_data_layout).when(
            lambda: self.session_store.has_property("access_token")
        ).register()
