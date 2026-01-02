from components import DataViewerComponent, SidebarComponent
from shared import ComponentIDs
from ststeroids import Layout


class ManageDataLayout(Layout):
    def __init__(self):
        self.sidebar = SidebarComponent.create(ComponentIDs.sidebar)
        self.data_viewer = DataViewerComponent.create(
            ComponentIDs.data_viewer, "Movies"
        )

    def render(self):
        self.sidebar.render()
        self.data_viewer.render()
