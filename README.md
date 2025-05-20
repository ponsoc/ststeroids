## StSteroids

A framework supercharging Streamlit for building advanced multi-page applications.


### Concepts

Ststeroids was designed to supercharge the development of complex multi-page applications while maintaining Streamlit’s simplicity. The framework emphasizes code reusability and separation of concerns, making it easier to manage multi-page setups. It enhances the maintainability of Streamlit applications and improves collaboration, enabling teams to work more effectively on a shared project.

The main concepts of Ststeroids are:

- Reusable Components
- Logics Flows
- Declarative Layouts
- Routers

In addition, StSteroids provides an easy way to load style sheets into your Streamlit application and offers a wrapper around `st.session_state` to separate states into stores. This wrapper is also used within components to store the component and its state in the session state.

#### Components
Components are at the core of StSteroids. A component represents a specific visual element of your application along with its rendering logic. Examples include a login dialog or a person details component.

Each component contains only the logic necessary for its functionality, such as basic input validation or button interactions that trigger a [flow](#flows). Components and their state are stored in the ComponentStore.

#### Flows
Flows contain the business logic of the application, handling its core functionality and, in some cases, linking components to backend services.

For example, a login flow might call an authentication service, validate the response, extract the access token, and store it in the session store.

#### Layouts
Layouts bring components together to create a multi-page application. Each layout functions as a page, rendering one or more components and defining their arrangement.

For example, a layout might define multiple Streamlit columns and place components within them.

#### Routers
Routers enable multi-page applications by defining routes and linking them to layouts. These routes are internal, meaning they cannot be accessed directly via a URL (due to current Streamlit limitations) and should be triggered through user interactions.

### Installation

```
pip install ststeroids
```

### Usage

StSteroids allows you to define components, layouts, and flows, then connect everything in `app.py` using a router. See the `example` folder in this repository.

To run the example app, execute the following commands from the project root:

```
pip install -r requirements.txt
streamlit run ./example/src/app.py
```

To run the tests, execute the following command from the project root:

```
pip install -r requirements.txt
pip install -r requirements-dev.txt
pytest
```

#### Components

Defining a new component.
```python
from ststeroids import Component

class YourXComponent(Component):
    def __init__(self, component_id: str):
        super().__init__(component_id) # This line is important to initialize the base class.

    def render(self):
        # Your render logic
```

Additionaly an initial state (dict) can be passed as a second paramters while initing the base class.

##### API Reference

`id`

Holds the component id

`state`

Manages the component state. Although technically an instance of the StSteroids `State` class, it functions like a dictionary, allowing properties to be accessed using getters and setters.  

When outside the component:
```python
myvalue = yourcomponent.state.yourproperty
yourcomponent.state.yourproperty = "yourvalue"
```

When inside the component:
```python
myvalue = self.state.yourproperty
self.state.yourproperty = "yourvalue"
```

`render()`

Renders an instance of the component.

`render_as_fragment(refresh_interval:str="5s", refresh_flow: Flow=None)`

Renders an instance of the component as a fragement. Additionality you can pass a refresh flow that should be called prior to rendering the component, you can use this to refresh the applications state.

`register_element(element_name: str)`

Registers a Streamlit element onto the component by generating component bound key. Use this function when setting a key for an element within the component.

Usage:

```python
    st.text_input("yourtext", key=self.register_element("yourtext"))
```

`get_element(element_name: str)`

Returns the value of a registered element.

Usage:

```python
    def yourbutton_click(self);
        yourtext = self.get_element("yourtext")

    st.text_input("yourtext",key=self.register_element("yourtext"))        
    st.button("yourbutton", on_click=self.yourbutton_click)
```

`set_element(element_name: str, element_value)`

Sets the value of a registered element.

#### Flows

Defining a new flow.
```python
from ststeroids import Flow

class YourXFlow(Flow):
    def __init__(self):
        super().__init__() # This line is important to initialize the base class.

    def run(self):
        # Your flow logic
```

##### API Reference

`component_store`

The component store containing the instances of components and their states.

Use `component_store.get_component(component_id: str)` to retrieve an instance of a component.

```python
from components import YourXComponent

your_x_component_instance: YourXComponent = self.component_store.get_component("your_x_component_id")
```

Notice the `: YourXComponent` this tells your IDE what type of component you are getting and helps the autocomplete.

#### Layouts

Defining a new layout.
```python
from ststeroids import Layout

class YourXLayout(Layout):
    def __init__(self):

    def run(self):
        # Your layout render logic
```

An instance of a layout can be rendered by calling either the `render()` function or by calling the instance of the layout.

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

#### Store

A wrapper around `st.session_state` to separate states into stores.

Usage:

```python
session_store = Store("yourstore")
```

##### API reference

`has_property(property_name: str)`

Checks if a property exists in the store.

`get_property(property_name: str)`

Retrieves the value of a property from the store.

`set_property(property_name: str)`

Sets the value of a property in the store.

#### Style

A helper class to easily apply CSS to your Streamlit Application.

Usage:

```python
from ststeroids import Style

app_style = Style("style.css")
app_style.apply_style()
```

### Release notes

0.1.13

- Adds a function to set a registered element's value
- Adds a function for rendering a component as a fragement

0.1.12

- Makes a real Singleton of the component store
- Fixes that an invalid route exception was thrown when an error occurred while running the layout beloning to a route, instead of throwing the real error.
- Updates the readme and the example on how to have better autocomplete

0.1.11

Considered first stable release

< 0.1.11

Beta releases

### Todo

- Improve IDE/autocomplete for state managed variables
- Automate test workflow and publish to pypi
- Ambition: directly link element values to component states
- Describe component store