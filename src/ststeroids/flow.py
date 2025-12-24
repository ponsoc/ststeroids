from abc import ABC, abstractmethod


# pylint: disable=too-few-public-methods
class Flow(ABC):
    """
    Base class for a flow
    """

    def execute_run(self, *args, **kwargs):
        """
        Executes the run method implemented in the subclasses.
        """
        return self.run(*args, **kwargs)

    @abstractmethod
    def run(self, *args, **kwargs):
        """
        Abstract methods that executes the flow logic.

        Each derived class should implement its own `run` method.

        :param args: Positional arguments for the run method.
        :param kwargs: Keyword arguments for the run method.
        """
        pass
