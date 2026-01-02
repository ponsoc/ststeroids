import streamlit as st
from ststeroids import Component


class SidebarComponent(Component):

    def display(self):
        with st.sidebar:
            st.page_link(
                "pages/dashboard.py", icon=":material/search:", label="Dashboard"
            )
            st.page_link(
                "pages/manage.py", icon=":material/bar_chart:", label="Manage data"
            )
