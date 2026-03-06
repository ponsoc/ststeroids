from ststeroids import Flow, FlowContext


class SetupFlow(Flow):
    def run(self, _ctx: FlowContext):
        print("I'm a flow setting up the app per user")
