import uuid
import streamlit as st
from ststeroids import Component


class DataViewerComponent(Component):
    def __init__(
        self,
        component_id: str,
        header: str,
        column_config: dict = {},
        column_order: list = [],
    ):
        super().__init__(component_id, {"data": None, "dek": uuid.uuid4()})
        self.header = header
        self.column_config = column_config
        self.column_order = column_order

    def render(self):
        st.subheader(self.header)
        st.dataframe(
            self.state.data,
            hide_index=True,
            column_config=self.column_config,
            column_order=self.column_order,
        )

    def set_data(self, data):
        self.state.data = data
