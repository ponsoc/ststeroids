from .route import Route


class RouteBuilder:
    def __init__(self, app, name: str):
        self.app = app
        self._name = name
        self._target = None
        self._condition = None

    def to(self, target):
        self._target = target
        return self

    def when(self, condition: callable):
        self._condition = condition
        return self

    def register(self):
        self.app.register(Route(self._name, self._target, self._condition))
