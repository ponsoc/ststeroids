from service import MockBackendService
from ststeroids import Flow, Store


class LoginFlow(Flow):
    def __init__(self, session_store: Store, backend_service: MockBackendService):
        super().__init__()
        self.session_store = session_store
        self.backend_service = backend_service

    def run(self, username: str, password: str):
        response = self.backend_service.authenticate(username, password)
        if response.ok:
            token_data = response.json()
            self.session_store.set_property("access_token", token_data["access_token"])
            return True
        return False
