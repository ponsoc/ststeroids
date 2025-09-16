from collections import defaultdict
import streamlit as st
from components import SidebarComponent
from flows import LoginFlow, LoginSuccessFlow, RefreshFlow
from layouts import LoginLayout, DashboardLayout, ManageDataLayout
from service import MockBackendService
from ststeroids import Router, Store, Style

class MainApp:

    def __init__(self):
        self.session_store = Store("store")
        self.router = Router("login")

        self.backend_service = MockBackendService("./example/test_data.json")
        self.login_flow = LoginFlow(self.session_store, self.backend_service)
        self.login_success_flow = LoginSuccessFlow(self.router, self.session_store, self.backend_service)
        self.refresh_flow = RefreshFlow(self.session_store, self.backend_service)

        st.set_page_config(page_title="StSteroids Example app", layout="wide")

        app_style = Style("./example/src/assets/style.css")
        app_style.apply_style()

        self.login_layout = LoginLayout("App login", self.login_flow, self.login_success_flow)
        self.dashboard_layout = DashboardLayout(self.refresh_flow)
        self.manage_data_layout = ManageDataLayout()

        self.sidebar = SidebarComponent("sidebar", self.router)
    
    def run(self, entry_route:str = None):
        self.sidebar.render()

        def get_routes():
            routes = defaultdict(lambda: self.login_layout)
            routes["login"] = self.login_layout

            if self.session_store.has_property("access_token"):
                routes.update(
                    {
                        "dashboard": self.dashboard_layout,
                        "manage_data": self.manage_data_layout,
                    },
                )

            return routes

        self.router.register_routes(get_routes())
        if entry_route:
            self.router.route(entry_route)
        self.router.run()
