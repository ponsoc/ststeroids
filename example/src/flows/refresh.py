import streamlit as st
from service import MockBackendService
from shared import ComponentIDs
from ststeroids import Flow, Store
from components import MetricComponent


class RefreshFlow(Flow):
    def __init__(
        self,
        session_store: Store,
        backend_service: MockBackendService,
        refresh_interval: str = "5s",
    ):
        super().__init__()
        self.session_store = session_store
        self.backend_service = backend_service
        self.refresh_interval = refresh_interval

    def run(self):
        @st.fragment(run_every=self.refresh_interval)
        def _run():
            cp_avg_rating: MetricComponent = self.component_store.get_component(
                ComponentIDs.avg_rating
            )
            response = self.backend_service.get_movies()
            if response.ok:
                data = response.json()
                self.session_store.set_property(
                    "data", data
                )  # Store the data in the session_store for later use in more complex applications
                avg_rating = self.avg_rating(data, "rating")
                cp_avg_rating.set_value(avg_rating)

        _run()

    def avg_rating(self, data, key):
        values = [d[key] for d in data if key in d and isinstance(d[key], (int, float))]
        return round(sum(values) / len(values)) if values else 0
