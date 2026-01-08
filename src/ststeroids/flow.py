from abc import ABC, abstractmethod
from.flow_context import FlowContext


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

    def dispatch(self, ctx: FlowContext) -> None:
        """
        Dispatches the flow execution.

        This method triggers the flow and forwards the context of the
        source that caused the execution.

        :param ctx: The `context` provides contextual information about what triggered the flow.
        :return: None
        """
        self.run(ctx)

    @abstractmethod
    def run(self, ctx: FlowContext) -> None:
        """
        Executes the flow logic.

        This method must be implemented by subclasses and contains the
        orchestration and business logic for the flow.

        :param ctx:  The `context` provides contextual information about what triggered the flow. Can be useful when you want to reuse a flow for different instances of the same component.
        :return: None
        """
        pass
