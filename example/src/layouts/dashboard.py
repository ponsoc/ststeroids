import streamlit as st
from components import (
    MetricComponent,
    SidebarComponent,
    ToastComponent,
    ButtonComponent,
)
from shared import ComponentIDs
from ststeroids import Layout, Flow


class DashboardLayout(Layout):
    def __init__(self, refresh_flow: Flow):
        self.refresh_flow = refresh_flow
        self.sidebar = SidebarComponent.create(ComponentIDs.sidebar)
        self.toast = ToastComponent.create(ComponentIDs.toast)
        self.total_movies = MetricComponent.create(
            ComponentIDs.total_movies, None, "Total movies"
        )
        self.avg_rating = MetricComponent.create(ComponentIDs.avg_rating, "2s", "Avg. Rating")
        self.logout_button = ButtonComponent.create(ComponentIDs.logout, "Logout")

    def render(self):
        self.sidebar.render()
        self.toast.render()
        left, right = st.columns([1, 1])
        with left:
            self.total_movies.render()
        with right:
            self.avg_rating.render()
        st.divider()
        self.logout_button.render()
