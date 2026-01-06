from ststeroids import Flow, Store


class LogoutFlow(Flow):
    def __init__(self, session_store: Store):
        self.session_store = session_store

    def run(self, component_id: str | None = None):
        self.session_store.del_property("access_token")
