import streamlit as st
from ststeroids import Component, Router


class SidebarComponent(Component):

    def __init__(self, component_id: str, router: Router):
        super().__init__(component_id)
        self.router = router

    def render(self):
        with st.sidebar:
            st.page_link("pages/dashboard.py", icon=":material/search:", label="Dashboard")
            st.page_link("pages/manage.py", icon=":material/bar_chart:", label="Manage data")
     
