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

    def execute_render(self):
        """
        Executes the render method implemented in the subclasses.
        """
        self.render()

    @abstractmethod
    def render(self) -> None:
        """
        Abstract method for rendering the layout.

        This method should be implemented by subclasses to define how the layout is rendered.
        """
        pass
