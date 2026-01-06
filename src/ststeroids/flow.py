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

    def dispatch(self, component_id: str | None = None) -> None:
        """
        Dispatches the flow execution.

        This method triggers the flow and forwards the identifier of the
        source that caused the execution.

        :param component_id: Optional identifier of the source component that triggered the flow. Ignore for other sources.
        :return: None
        """
        return self.run(component_id)

    @abstractmethod
    def run(self, component_id: str | None = None) -> None:
        """
        Executes the flow logic.

        This method must be implemented by subclasses and contains the
        orchestration and business logic for the flow.

        The `component_id` provides contextual information about which component triggered
        the flow.

        :param component_id: Optional identifier of the source component that triggered the flow. Can be useful when you want to reuse a flow for different instances of the same component.
        :return: None
        """
        pass
