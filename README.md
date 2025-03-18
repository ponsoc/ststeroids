## StSteroids

A framework supercharging Streamlit for building advanced multi-page applications.


### Concepts

Ststeroids was designed to supercharge the development of complex multi-page applications while maintaining Streamlit’s simplicity. The framework emphasizes code reusability and separation of concerns, making it easier to manage multi-page setups. It enhances the maintainability of Streamlit applications and improves collaboration, enabling teams to work more effectively on a shared project.

The main concepts of Ststeroids are:

- Components
- Flows
- Layouts
- Routers

In addition it comes with an easy way of loading style sheets into your Streamlit application.

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

#### Component

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

#### Flow

Defining a new flow.
```python
from ststeroids import Flow

class YourXFlow(Flow)
    def __init__(self)
        super().__init__() # This line is important to initialize the base class.

    def run(self)
        # Your flow logic
```

### Todo

- Add test
- Update readme
- Add example project structure