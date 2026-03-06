from service import MockBackendService
from ststeroids import Flow, Store, FlowContext
from components import (
    LoginDialogComponent,
    DataViewerComponent,
    MetricComponent,
    ToastComponent,
)
from shared import ComponentIDs
import streamlit as st


class LoginFlow(Flow):
    def __init__(self, session_store: Store, backend_service: MockBackendService):
        self.session_store = session_store
        self.backend_service = backend_service

    @property
    def cp_login_dialog(self):
        return LoginDialogComponent.get(ComponentIDs.dialog_login)

    @property
    def cp_data_viewer(self):
        return DataViewerComponent.get(ComponentIDs.data_viewer)

    @property
    def cp_total_movies(self):
        return MetricComponent.get(ComponentIDs.total_movies)

    @property
    def cp_toast(self):
        return ToastComponent.get(ComponentIDs.toast)

    def run(self, _ctx: FlowContext):
        response = self.backend_service.authenticate(
            self.cp_login_dialog.username, self.cp_login_dialog.password
        )
        if response.ok:
            self._login_success(response)
        else:
            self._login_failed()

    def _login_success(self, response):
        token_data = response.json()
        self.session_store.set_property("access_token", token_data["access_token"])
        self.cp_login_dialog.hide()
        response = self.backend_service.get_movies()
        # enable the line below for example of an error scenario
        # response.ok = False
        if response.ok:
            data = response.json()
            self.session_store.set_property(
                "data", data
            )  # Store the data in the session_store for later use in more complex applications
            self.cp_total_movies.set_value(len(data))
            self.cp_data_viewer.set_data(data)
        else:
            self.cp_toast.set_message("error")
        st.switch_page("pages/dashboard.py")

    def _login_failed(self):
        self.cp_login_dialog.set_error("Login failed, check your username and password")
