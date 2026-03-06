import streamlit as st
from ststeroids import Fragment


class MetricComponent(Fragment):
    def __init__(
        self,
        header: str,
    ):
        self.header = header
        self.value = 0

    def display(self):
        st.metric(self.header, self.value)

    def set_value(self, value: int):
        self.value = value
