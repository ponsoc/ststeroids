from components import DataViewerComponent
from shared import ComponentIDs
from ststeroids import Layout


class ManageDataLayout(Layout):
    def __init__(self):
        self.data_viewer = DataViewerComponent(ComponentIDs.data_viewer, "Movies")

    def render(self):
        self.data_viewer.render()
