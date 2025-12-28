## StSteroids

A framework supercharging Streamlit for building advanced multi-page applications.


### Concepts

Ststeroids was designed to supercharge the development of complex multi-page applications while maintaining Streamlit’s simplicity. The framework emphasizes code reusability and separation of concerns, making it easier to manage multi-page setups. It enhances the maintainability of Streamlit applications and improves collaboration, enabling teams to work more effectively on a shared project.

The main concepts of Ststeroids are:

- Reusable Components
- Logic Flows
- Declarative Layouts
- A Router
- A Store

In addition, StSteroids provides an easy way to load style sheets into your Streamlit application and offers a wrapper around `st.session_state` to separate states into stores. This wrapper is also used within components to store the component and its state in the session state.

#### Components
Components are at the core of StSteroids. A component represents a specific visual element of your application along with its rendering logic. Examples include a login dialog or a person details component.

Each component contains only the logic necessary for its functionality, such as basic input validation or button interactions that trigger a [flow](#flows). Components and their attributes are stored in the ComponentStore which is a special instance of a Store.

Component concepts:

- components never decide on domain logic, so no domain error handeling for example
- a component contains interaction elements, unless
    - the component is still meaningful and usable without a the interaction element → split the element out
- a component doesn't navigate pages
- should have functions for updating it's attributes (explicit state changes) (so that the flow doesn't need to all the attributes)

For example, a metric component that can be reused for multiple purposes.

#### Flows

Flows encapsulate the application’s interaction and orchestration logic.  
They handle user-initiated actions, coordinate state changes across components, and invoke domain services to perform business operations.

Flow concepts:

- Flows act as handlers for user and system interactions (e.g. button clicks, page entry, form submission)
- Flows orchestrate application behavior, calling services and updating component state
- Flows coordinate multiple components and stores as part of a single interaction
- Flows determine navigation and control flow between layouts or pages
- Flows own error handling and recovery logic for the interactions they manage
- Flows may contain light business rules, but core domain logic should live in services

For example, a login flow might call an authentication service, evaluate the result, store relevant session data, and update one or more components to reflect the outcome.

When multiple flows share orchestration resources—such as access to the same components, stores, or helper logic—it is recommended to introduce a shared base flow to centralize this responsibility and avoid duplication.

#### Layouts
Layouts bring components together to create a multi-page application. Each layout functions as a page, rendering one or more components and defining their arrangement and rendering.

Layout concepts:

- layouts are responsible for initializing and wiring components
- layouts are responsible for the visual arrangement of components
- layouts are responsible for conditional rendering based on application state or context (for example, authorisation)

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
streamlit run --client.showSidebarNavigation=False ./example/src/app.py
```

To run the tests, execute the following command from the project root:

```
pip install -r requirements.txt
pip install -r requirements-dev.txt
pytest
```

#### Components

Example of defining a new component.

```python
from ststeroids import Component

class MetricComponent(Component):
    def __init__(
        self,
        header: str,
    ):
        self.header = header
        self.value = 0

    def display(self):
        st.metric(self.header, self.value)

    def set_value(self, value: int):
        self.value = value
```

The header attribute and set_value method are specific to this example. They illustrate how components can have instance-bound attributes and provide an explicit API for updating their state. Components should own their state and expose such functions rather than allowing external code to directly mutate their attributes.

##### API Reference

`id`

Holds the component id, is automaticly added from the base component.

`create(cls, component_id: str, *args, **kwargs)`

Creates a new component instance with the given `component_id` and stores it in the `ComponentStore`.  
This is typically called in layouts to initialize components. Additional arguments are passed to the component's constructor.

`get(cls, component_id: str)`

Retrieves an existing component instance from the `ComponentStore` by its `component_id`.  
`create()` must have been called first; otherwise, an error will be raised.  
This is typically used in flows that needs to interact with a component after it has been initialized.

`display()`

This method needs to be implemented by the subclass. To call it in a layout, use `render()`

`render(render_as: Literal["normal", "dialog", "fragment"]="normal", options:dict={})`

Executes the display method of an instance of a component. Additionaly provide the `render_as` parameter with the `options` parameter.

Dialog options:

**title**

The dialog title.

Fragment options:

**refresh_flow**

A refresh flow that should be called post rendering the component, you can use this to refresh the applications state for the next view.

**refresh_interval**

The refresh interval, for example: `2s`.


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
        

    def run(self):
        # Your flow logic
```

<!-- ## example of shared resoruces here -->

##### API Reference

`run()`

This method needs to be implemented by the subclass. To call it, use `dispatch()`

`dispatch()`

Executes the run method implemented in the subclass.

#### Layouts

Example of defining a new layout.

```python
from ststeroids import Layout

class ManageDataLayout(Layout):
    def __init__(self):
        self.data_viewer = DataViewerComponent.create(
            ComponentIDs.data_viewer, "Movies"
        )

    def render(self):
        self.data_viewer.render()
```

An instance of a layout can be rendered by calling either the `render()` function.

Calling the instance
```python
my_x_layout = YourXLayout()
my_x_layout.render()
```
<!-- explain that this not must be done direclty but trough a router -->

##### API Reference

 `render()`

This method needs to be implemented by the subclass.

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

`set_property(property_name: str, property_value: str)`

Sets the value of a property in the store.

`del_property(property_name: str)`

Deletes the property from the store.

#### Style

A helper class to easily apply CSS to your Streamlit Application.

Usage:

```python
from ststeroids import Style

app_style = Style("style.css")
app_style.apply_style()
```

### Release notes

1.0.0

A partial rewrite of the framework so that it has a smaller footprint and creation of objects feels more natural and is better supported by editors and debuggers.

-

**Note** this version is considered to be a breaking change. Make sure to adapt your code base so that it works with this new version.

0.1.17

- Improved execute_render function by adding an error handler
- Default refresh_interval for a fragment is now `None` to avoid unintended refreshes

0.1.16

- Improved component instance creation by making component instances a singleton

0.1.15

- Added option to delete a property from the store

0.1.14

- Improved UI peformance when working with fragments.
- Improved method naming. **Note** to update the run and render calls to `execute_run` and `exectute_render`

0.1.13

- Adds a function to set a registered element's value.
- Adds a function for rendering a component as a fragment.

0.1.12

- Makes a real Singleton of the component store.
- Fixes that an invalid route exception was thrown when an error occurred while running the layout beloning to a route, instead of throwing the real error.
- Updates the readme and the example on how to have better autocomplete.

0.1.11

Considered first stable release.

< 0.1.11

Beta releases

### Todo

- Improve IDE/autocomplete for state managed variables
- Ambition: directly link element values to component states
- Describe component store
- Layout and flow class singletons

## Ideas

- Something for RBAC
- Something for running longtime requests