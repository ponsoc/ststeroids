import streamlit as st
from ststeroids import Component


class MetricComponent(Component):
    def __init__(
        self,
        component_id: str,
        header: str,
    ):
        super().__init__(component_id, {"value": None})
        self.header = header
        print("init")

    def render(self):
        st.metric(self.header, self.state.value)

    def set_value(self, value: int):
        self.state.value = value
