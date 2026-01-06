import streamlit as st
from components import MetricComponent, SidebarComponent, ToastComponent
from shared import ComponentIDs
from ststeroids import Layout, Flow


class DashboardLayout(Layout):
    def __init__(self, refresh_flow: Flow):
        self.refresh_flow = refresh_flow
        self.sidebar = SidebarComponent.create(ComponentIDs.sidebar)
        self.toast = ToastComponent.create(ComponentIDs.toast)
        self.total_movies = MetricComponent.create(
            ComponentIDs.total_movies, "Total movies"
        )
        self.avg_rating = MetricComponent.create(ComponentIDs.avg_rating, "Avg. Rating")

    def render(self):
        self.sidebar.render()
        self.toast.render()
        left, right = st.columns([1, 1])
        with left:
            self.total_movies.render()
        with right:
            self.avg_rating.render(
                "fragment",
                {"refresh_flow": self.refresh_flow, "refresh_interval": "2s"},
            )

        if st.button("logout"):
            del st.session_state["store"]["access_token"]
