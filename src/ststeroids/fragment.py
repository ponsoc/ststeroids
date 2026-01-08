from .component import Component
from .flow import Flow
import streamlit as st

class Fragment(Component):
    """
    Base class for components that render as Streamlit fragments and provide
    a built-in `refresh` event for decoupled flows.
    """

    refresh_interval: str
    EVENT_REFRESH = "_refresh"  # class-level constant for autocomplete

    @classmethod
    def create(cls, component_id: str, refresh_interval: str = "5s", *args, **kwargs):
        """
        Create a new Fragment instance or return it from the store.

        :param component_id: Unique identifier for this dialog component.
        :param refresh_interval: The interval for the on_refresh event.
        :return: Fragment instance
        """
        instance = super().create(component_id, *args, **kwargs)
        instance.refresh_interval = refresh_interval
        return instance

    def render(self):
        """
        Render the component as a fragment and trigger the `on_refresh` event
        on each rerun/refresh.
        """
        if not self.visible:
            return

        @st.fragment(run_every=self.refresh_interval)
        def _fragment():
            if self.EVENT_REFRESH in self._events:
                self.trigger(self.EVENT_REFRESH)
            self.display()

        _fragment()

    def on_refresh(self, flow: Flow) -> None:
        """
        Register a flow to be executed when the the fragment refreshes
        """
        self.on(self.EVENT_REFRESH, flow)
        