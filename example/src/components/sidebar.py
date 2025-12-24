import streamlit as st
from ststeroids import Component


class SidebarComponent(Component):

    def __init__(self, component_id: str):
        super().__init__(component_id)

    def _test(self):
        if "test" not in st.session_state:
            st.session_state["test"] = True
        if st.session_state["test"] == True:
            st.session_state["test"] = False
        else:
            st.session_state["test"] = True
        print(st.session_state["test"])

    def render(self):
        with st.sidebar:
            st.page_link("pages/dashboard.py", icon=":material/search:", label="Dashboard")
            st.page_link("pages/manage.py", icon=":material/bar_chart:", label="Manage data")
     
            st.button("test",key="testkey",on_click=self._test)