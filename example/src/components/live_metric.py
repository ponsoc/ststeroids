import streamlit as st
from ststeroids import Component


class LiveMetricComponent(Component):
    def __init__(self, component_id: str, header: str, resfresh_interval: str = "10s"):
        super().__init__(component_id, {"value": None})
        self.header = header
        self.resfresh_interval = resfresh_interval

    def render(self):
        @st.fragment(run_every=self.resfresh_interval)
        def _render():
            st.metric(self.header, self.state.value)

        _render()

    def set_value(self, value: int):
        self.state.value = value
