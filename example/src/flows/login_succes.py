from service import MockBackendService
from shared import ComponentIDs
from ststeroids import Flow, Store
from components import LoginDialogComponent, DataViewerComponent, MetricComponent
import streamlit as st


class LoginSuccessFlow(Flow):
    def __init__(self, session_store: Store, backend_service: MockBackendService):
        super().__init__()
        self.session_store = session_store
        self.backend_service = backend_service

    def run(self):
        cp_login_dialog = LoginDialogComponent.get(ComponentIDs.dialog_login)
        cp_data_viewer = DataViewerComponent.get(ComponentIDs.data_viewer)
        cp_total_movies = MetricComponent.get(ComponentIDs.total_movies)
        response = self.backend_service.get_movies()
        if response.ok:
            data = response.json()
            self.session_store.set_property(
                "data", data
            )  # Store the data in the session_store for later use in more complex applications
            cp_total_movies.set_value(len(data))
            cp_data_viewer.set_data(data)
        st.switch_page("pages/dashboard.py")
        cp_login_dialog.hide()
