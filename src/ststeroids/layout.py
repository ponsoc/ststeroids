class Layout:
    """
    Base class for a layout
    """

    def __call__(self):
        self.render()

    def render(self) -> None:
        """
        Placeholder method for rendering the layout.

        This method should be implemented by subclasses to define how the layout is rendered.

        :raises NotImplementedError: If called directly without being implemented in a subclass.
        """
        raise NotImplementedError("Subclasses should implement this method.")
