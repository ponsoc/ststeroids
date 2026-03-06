from typing import Literal

import streamlit as st
from ststeroids import Component


class StatusComponent(Component):

    def __init__(
        self,
        message: str = None,
        type: Literal["running", "info", "error", "success"] = "info",
    ):
        self.message = message
        self.type = type

    def display(self):
        if self.message:
            st.markdown(f"<div class='status-row'>{self._status_icon(self.type)}<div>{self.message}</div></div>", unsafe_allow_html=True)

    def set_status(self, message: str, type: Literal["running", "info", "error", "success"] = "info"):
        self.message = message
        self.type = type

    def clear(self):
        self.message = None
        self.type = None

    def _status_icon(self, state: str):
        icons = {"success": "✓", "error": "✕", "info": "i", "running": ""}

        return f"<div class='status-icon {state}'>{icons.get(state, '')}</div>"
