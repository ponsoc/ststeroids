import streamlit as st

class FlowContext:
    """
    Encapsulates the context of why a flow is being executed.

    Attributes:
        type: The type of the trigger ("component", "route", "app").
        identifier: Optional identifier, e.g., component id, route name.
    """

    type: str
    identifier: str = None

    def __init__(self, type: str, identifier: str):
        self.type = type
        self.identifier = identifier

    def schedule_and_rerun(self, fn, *args, **kwargs):
        self.schedule(fn, *args, **kwargs)
        st.rerun()

    def schedule(self, fn, *args, **kwargs):
        st.session_state["_schedule_rerun"] = {
            "fn": fn,
            "args": args,
            "kwargs": kwargs,
            "type": self.type,
            "identifier": self.identifier,
        }