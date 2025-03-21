from shared import ComponentIDs
from ststeroids import Flow, Router


class LoginSuccessFlow(Flow):
    def __init__(self, router: Router):
        super().__init__()
        self.router = router

    def run(self):
        login_dialog = self.component_store.get_component(ComponentIDs.dialog_login)
        self.router.route("dashboard")
        login_dialog.hide()

