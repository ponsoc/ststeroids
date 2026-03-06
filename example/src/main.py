import streamlit as st
from flows import LoginFlow, RefreshFlow, SetupFlow, LogoutFlow, LongRunningFlow
from layouts import LoginLayout, DashboardLayout, ManageDataLayout
from service import MockBackendService
from ststeroids import Store, Style, StSteroids


class MainApp:

    def __init__(self):
        self.session_store = Store.create("store")

        self.backend_service = MockBackendService("./example/test_data.json")
        self.setup_flow = SetupFlow.create()
        self.login_flow = LoginFlow.create(self.session_store, self.backend_service)
        self.logout_flow = LogoutFlow.create(self.session_store)
        self.refresh_flow = RefreshFlow.create(self.session_store, self.backend_service)
        self.long_running_flow = LongRunningFlow.create()

        st.set_page_config(page_title="StSteroids Example app", layout="wide")

        app_style = Style("./example/src/assets/style.css")
        app_style.apply_style()

        self.login_layout = LoginLayout.create(self.session_store, "App login")
        self.dashboard_layout = DashboardLayout.create(self.refresh_flow)
        self.manage_data_layout = ManageDataLayout.create()

        # register event handlers
        self.login_layout.login_dialog.on_login(self.login_flow)
        self.dashboard_layout.long_running_button.on_click(self.long_running_flow)
        self.dashboard_layout.logout_button.on_click(self.logout_flow)
        self.dashboard_layout.avg_rating.on_refresh(self.refresh_flow)

        self.app = StSteroids()

        self.app.on_app_run_once(self.setup_flow)

        self.app.default_route(self.login_layout)

        self.app.route("login").to(self.login_layout).register()
        self.app.route("dashboard").to(self.dashboard_layout).when(lambda: self.session_store.has_property("access_token")).register()
        self.app.route("manage_data").to(self.manage_data_layout).when(lambda: self.session_store.has_property("access_token")).register()
