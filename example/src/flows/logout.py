from ststeroids import Flow, Store, FlowContext


class LogoutFlow(Flow):
    def __init__(self, session_store: Store):
        self.session_store = session_store

    def run(self, _ctx: FlowContext ):
        self.session_store.del_property("access_token")
