from abc import ABC, abstractmethod


class Layout(ABC):
    """
    Base class for a layout
    """

    @classmethod
    def create(cls, *args, **kwargs):
        """
        Creates a new layout instance.
        """
        return cls(*args, **kwargs)

    @abstractmethod
    def render(self) -> None:
        """
        Abstract method for rendering the layout.

        This method should be implemented by subclasses to define how the layout is rendered.
        """
        pass
