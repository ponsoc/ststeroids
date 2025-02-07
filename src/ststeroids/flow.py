from .store import ComponentStore


class Flow:
    def __init__(self):
        self.component_store = ComponentStore()

    def run(self):
        """
        Each derived class should implement its own run logic.
        """
        raise NotImplementedError("Subclasses must implement the run method.")
