from typing import Any
from .store import ComponentStore

class Component:
    """
    Base class for a component that interacts with the state and the store.
    
    Attributes:
        id (str): The unique identifier for the component.
        state (State): The state associated with the component.
    """
    
    def __init__(self, component_id: str, initial_state: dict = {}):
        """
        Initializes the component with a unique ID and initial state.
        
        :param component_id: The unique identifier for the component.
        :param initial_state: Initial state for the component. Defaults to an empty dictionary.
        """
        self.__store = ComponentStore()
        self.id = component_id
        self.state = State(self.id, self.__store, initial_state)
        self.__store.init_component(self)

    def render(self) -> None:
        """
        Calls the derived class's render method if the layout is visible.
        If not, it prevents rendering.
        
        :raises NotImplementedError: If called directly without being implemented in a subclass.
        """
        if not self.state.visible:
            return  # Do nothing if not visible
        
        # Delegate rendering to the subclass
        self._render()             
        

    def _render(self) -> None:
        """
        Placeholder method for rendering the component.
        
        This method should be implemented by subclasses to define how the component is rendered.
        
        :raises NotImplementedError: If called directly without being implemented in a subclass.
        """
        raise NotImplementedError("Subclasses should implement this method.")

class Layout:
    """
    Base class for a layout that interacts with the state and the store.
    
    Attributes:
        id (str): The unique identifier for the layout.
    """
    
    def __init__(self, layout_id: str, visible: bool):
        """
        Initializes the layout with a unique ID.
        
        :param layout_id: The unique identifier for the layout.
        """
        self.__store = ComponentStore()
        self.id = layout_id
        self.state = State(self.id, self.__store, {"visible":visible})
        self.__store.init_component(self)

    def render(self) -> None:
        """
        Calls the derived class's render method if the layout is visible.
        If not, it prevents rendering.
        
        :raises NotImplementedError: If called directly without being implemented in a subclass.
        """
        if not self.state.visible:
            return  # Do nothing if not visible
        
        # Delegate rendering to the subclass
        self._render()            

    def _render(self) -> None:
        """
        Placeholder method for rendering the layout.
        
        This method should be implemented by subclasses to define how the layout is rendered.
        
        :raises NotImplementedError: If called directly without being implemented in a subclass.
        """
        raise NotImplementedError("Subclasses should implement this method.")
    
    def hide(self) -> None:
        self.state.visibile = False

    def unhide(self) -> None:
        self.state.visibile = True

class State:
    """
    Manages the state of a component, storing and retrieving properties through the associated store.
    
    Attributes:
        __id (str): The unique identifier for the component.
        __store (ComponentStore): The store instance that holds the component's state.
    """
    
    def __init__(self, component_id: str, store: ComponentStore, initial_state: dict):
        """
        Initializes the state for a component, setting up the store and component ID.
        
        :param component_id: The unique identifier for the component.
        :param store: The store instance where the state is stored.
        :param initial_state: Initial state data for the component.
        """
        super().__setattr__("_State__id", component_id)  # Directly set private attributes
        super().__setattr__("_State__store", store)      # Avoid recursion
        store.init_component_state(component_id, initial_state)
    
    def __getattr__(self, name) -> Any:
        """
        Retrieves a property of the component from the store.
        
        :param name: The name of the property to retrieve.
        :return: The value of the property from the store.
        
        :raises AttributeError: If the requested property is not found.
        """
        if not name.startswith("__"):
            return self.__store.get_property(self.__id, name)
        raise AttributeError(f"'{type(self).__name__}' object has no attribute '{name}'")

    def __setattr__(self, name, value):
        """
        Sets a property of the component in the store.
        
        :param name: The name of the property to set.
        :param value: The value to set for the property.
        
        This method avoids recursion for special attributes and handles normal properties.
        """
        if not name.startswith("__"):
            self.__store.set_property(self.__id, name, value)
        else:
            super().__setattr__(name, value)  # Avoid recursion for special attributes