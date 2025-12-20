from components import DataViewerComponent, SidebarComponent
from shared import ComponentIDs
from ststeroids import Layout


class ManageDataLayout(Layout):
    def __init__(self):
        self.data_viewer = DataViewerComponent(ComponentIDs.data_viewer, "Movies")
        self.sidebar = SidebarComponent("sidebar")

    def render(self):
        self.sidebar.execute_render()
        self.data_viewer.render()
