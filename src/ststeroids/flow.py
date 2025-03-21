from .store import ComponentStore


# pylint: disable=too-few-public-methods
class Flow:
    """
    Base class for a flow that can interact with the component store
    """

    def __init__(self):
        """
        Initializes the Flow class and creates a ComponentStore instance.
        """
        self.component_store = ComponentStore()

    def run(self, *args, **kwargs):
        """
        Executes the flow logic.

        Each derived class should implement its own `run` method.

        :param args: Positional arguments for the run method.
        :param kwargs: Keyword arguments for the run method.
        :return: None
        :raises NotImplementedError: If the method is not implemented in a subclass.
        """
        raise NotImplementedError("Subclasses must implement the run method.")
