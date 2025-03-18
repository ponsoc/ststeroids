## StSteroids

A framework supercharging Streamlit for building advanced multi-page applications.


### Concepts

Ststeroids was designed to supercharge the development of complex multi-page applications while maintaining Streamlit’s simplicity. The framework emphasizes code reusability and separation of concerns, making it easier to manage multi-page setups. It enhances the maintainability of Streamlit applications and improves collaboration, enabling teams to work more effectively on a shared project.

The main concepts of Ststeroids are:

- Components
- Flows
- Layouts
- Routers

In addition, StSteroids provides an easy way to load style sheets into your Streamlit application and offers a wrapper around `st.session_state` to separate states into stores. This wrapper is also used within components to store the component and its state in the session state.

#### Components
Components are at the core of StSteroids. A component represents a specific visual element of your application along with its rendering logic. Examples include a login dialog or a person details component.

Each component contains only the logic necessary for its functionality, such as basic input validation or button interactions that trigger a [flow](#flows). Components and their state are stored in the ComponentStore.

### Flows
Flows contain the business logic of the application, handling its core functionality and, in some cases, linking components to backend services.

For example, a login flow might call an authentication service, validate the response, extract the access token, and store it in the session store.

### Layouts
Layouts bring components together to create a multi-page application. Each layout functions as a page, rendering one or more components and defining their arrangement.

For example, a layout might define multiple Streamlit columns and place components within them.

### Routers
Routers enable multi-page applications by defining routes and linking them to layouts. These routes are internal, meaning they cannot be accessed directly via a URL (due to current Streamlit limitations) and should be triggered through user interactions.

### Usage

StSteroids allows you to define components, layouts, and flows, then connect everything in `app.py` using a router. See the `example` folder in this repository.

#### Components

Defining a new component.
```python
from ststeroids import Component

class YourXComponent(Component)
    def __init__(self, component_id: str)
        super().__init__(component_id) # This line is important to initialize the base class.

    def render(self)
        # Your render logic
```

Additionaly an initial state (dict) can be passed as a second paramters while initing the base class.

##### API Reference

`id`

Holds the component id

`state`

Manages the component state. Although technically an instance of the StSteroids `State` class, it functions like a dictionary, allowing properties to be accessed using getters and setters.  

When outside the component:
```
myvalue = yourcomponent.state.yourproperty
yourcomponent.state.yourproperty = "yourvalue"
```

When inside the component:
```
myvalue = self.state.yourproperty
self.state.yourproperty = "yourvalue"
```

#### Flows

Defining a new flow.
```python
from ststeroids import Flow

class YourXFlow(Flow)
    def __init__(self)
        super().__init__() # This line is important to initialize the base class.

    def run(self)
        # Your flow logic
```

##### API Reference

`component_store`

The component store containing the instances of components and their states.

Use `component_store.get_component(component_id: str)` to retrieve an instance of a component.

#### Layouts

Defining a new layout.
```python
from ststeroids import Layout

class YourXLayout(Layout)
    def __init__(self)

    def run(self)
        # Your layout render logic
```

An instance of a layout can be renderd by calling either the `render()` function or by calling the instance of the layout.

Calling the instance
```python
my_x_layout = YourXLayout()
my_x_layout()
```

#### Routers
Intializing a router

```python
from ststeroids import Router
router = Router()
```

##### API Reference

`run`

Runs the currently active route

`route(route_name: str)`

Changes the currently active to the given route name

`register_routes(routes: dict[str, Layout])`

Registers a dictionary of routes where keys are route names and values are layouts.

`get_current_route`

Returns the currently active route. Useful for creating a navigation breadcrumbs. 

### Todo

- Add test
- Add example project structure