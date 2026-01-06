from ststeroids import Flow


class SetupFlow(Flow):
    def run(self, component_id: str | None = None):
        print("I'm a flow setting up the app per user")
