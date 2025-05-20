from service import MockBackendService
from shared import ComponentIDs
from ststeroids import Flow, Router, Store
from components import LoginDialogComponent, DataViewerComponent, MetricComponent


class LoginSuccessFlow(Flow):
    def __init__(
        self, router: Router, session_store: Store, backend_service: MockBackendService
    ):
        super().__init__()
        self.session_store = session_store
        self.backend_service = backend_service
        self.router = router

    def run(self):
        cp_login_dialog: LoginDialogComponent = self.component_store.get_component(
            ComponentIDs.dialog_login
        )
        cp_data_viewer: DataViewerComponent = self.component_store.get_component(
            ComponentIDs.data_viewer
        )
        cp_total_movies: MetricComponent = self.component_store.get_component(
            ComponentIDs.total_movies
        )
        response = self.backend_service.get_movies()
        if response.ok:
            data = response.json()
            self.session_store.set_property(
                "data", data
            )  # Store the data in the session_store for later use in more complex applications
            cp_total_movies.set_value(len(data))
            cp_data_viewer.set_data(data)
        self.router.route("dashboard")
        cp_login_dialog.hide()
