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

    def dispatch(self) -> None:
        """
        Executes the run method implemented in the subclasses.
        """
        return self.run()

    @abstractmethod
    def run(self) -> None:
        """
        Abstract methods that executes the flow logic.

        Each derived class should implement its own `run` method.
        """
        pass
