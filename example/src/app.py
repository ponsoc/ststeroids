import streamlit as st
from collections import defaultdict
from components import SidebarComponent
from flows import (
    LoginFlow,
    LoginSuccessFlow,
)
from layouts import LoginLayout, DashboardLayout, ManageDataLayout
from service import MockBackendService
from ststeroids import Router, Store, Style

session_store = Store("store")
router = Router("login")

backend_service = MockBackendService("./example/test_data.json")
login_flow = LoginFlow(session_store, backend_service)
login_success_flow = LoginSuccessFlow(router, session_store, backend_service)

st.set_page_config(layout="wide")

app_style = Style("./example/src/assets/style.css")
app_style.apply_style()

login_layout = LoginLayout("App login", login_flow, login_success_flow)
dashboard_layout = DashboardLayout()
manage_data_layout = ManageDataLayout()

sidebar = SidebarComponent("sidebar", router)
sidebar.render()


def get_routes():
    routes = defaultdict(lambda: login_layout)
    routes["login"] = login_layout

    if session_store.has_property("access_token"):
        routes.update(
            {
                "dashboard": dashboard_layout,
                "manage_data": manage_data_layout,
            },
        )

    return routes


router.register_routes(get_routes())

router.run()
