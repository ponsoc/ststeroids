import streamlit as st
from components import (
    MetricComponent,
    SidebarComponent,
    ToastComponent,
    ButtonComponent,
    StatusComponent
)
from shared import ComponentIDs
from ststeroids import Layout, Flow


class DashboardLayout(Layout):
    def __init__(self, refresh_flow: Flow):
        self.refresh_flow = refresh_flow
        self.sidebar = SidebarComponent.create(ComponentIDs.sidebar)
        self.status = StatusComponent.create(ComponentIDs.spinner)
        self.toast = ToastComponent.create(ComponentIDs.toast)
        self.total_movies = MetricComponent.create(
            ComponentIDs.total_movies, None, "Total movies"
        )
        self.avg_rating = MetricComponent.create(
            ComponentIDs.avg_rating, "2s", "Avg. Rating"
        )
        self.logout_button = ButtonComponent.create(ComponentIDs.logout, "Logout")
        self.long_running_button = ButtonComponent.create(ComponentIDs.long_running, "Long running call")

    def render(self):
        self.sidebar.render()
        self.toast.render()
        left, right = st.columns([1, 1])
        with left:
            self.total_movies.render()
        with right:
            self.avg_rating.render()
        self.status.render()
        st.divider()
        self.long_running_button.render()
        self.logout_button.render()
