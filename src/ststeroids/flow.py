from abc import ABC, abstractmethod


# pylint: disable=too-few-public-methods
class Flow(ABC):
    """
    Base class for a flow
    """

    @classmethod
    def create(cls, *args, **kwargs):
        """
        Creates a new flow instance.
        """
        return cls(*args, **kwargs)

    def dispatch(self):
        """
        Executes the run method implemented in the subclasses.
        """
        return self.run()

    @abstractmethod
    def run(self):
        """
        Abstract methods that executes the flow logic.

        Each derived class should implement its own `run` method.

        :param args: Positional arguments for the run method.
        :param kwargs: Keyword arguments for the run method.
        """
        pass
