import streamlit as st
from ststeroids import Component, Flow, Router


class SidebarComponent(Component):

    def __init__(self, component_id: str, router: Router):
        super().__init__(component_id)
        self.router = router

    def __on_menu_item_click(self, item):
        self.router.route(item)

    def __get_titles(self):
        current_route = self.router.get_current_route()
        dashboard_title = "Dashboard"
        manage_data_title = "Manage data"

        if current_route == "dashboard":
            dashboard_title = f"**:primary-background[{dashboard_title}]**"
        if current_route == "manage_data":
            manage_data_title = f"**:primary-background[{manage_data_title}]**"

        return dashboard_title, manage_data_title

    def render(self):
        dashboard_title, manage_data_title = self.__get_titles()
        with st.sidebar:
            st.button(dashboard_title, icon=":material/search:", type="tertiary", on_click=self.__on_menu_item_click, kwargs={"item": "dashboard"})
            st.button(manage_data_title, icon=":material/bar_chart:", type="tertiary", on_click=self.__on_menu_item_click, kwargs={"item": "manage_data"})