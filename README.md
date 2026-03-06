## StSteroids

A framework supercharging Streamlit for building advanced multi-page applications.


### Concepts

Ststeroids was designed to supercharge the development of complex multi-page applications while maintaining Streamlit’s simplicity. The framework emphasizes code reusability and separation of concerns, making it easier to manage multi-page setups. It enhances the maintainability of Streamlit applications and improves collaboration, enabling teams to work more effectively on a shared project.

The main concepts of Ststeroids are:

- Reusable Components
- Logic Flows
- Declarative Layouts
- A Store

In addition, StSteroids provides an easy way to load style sheets into your Streamlit application and offers a wrapper around `st.session_state` to separate states into stores. This wrapper is also used within components to store the component and its state in the session state.

#### Components
Components are at the core of StSteroids. A component represents a specific visual element of your application along with its rendering logic. Examples include a login dialog or a person details component.

Each component contains only the logic necessary for its functionality, such as basic input validation or button interactions that trigger a [flow](#flows). Components and their attributes are stored in the ComponentStore which is a special instance of a Store.

Component concepts:

- components never decide on domain logic, so there is no domain error handling for example
- a component contains interaction elements, unless the component is still meaningful and usable without the interaction element → split the element out
- components don't navigate pages
- should have methods for updating its attributes (explicit state changes so that the flow doesn't need to all the attributes)

For example, a metric component that can be reused for multiple purposes.

#### Flows

Flows encapsulate the application’s interaction and orchestration logic.  
They handle user-initiated actions, coordinate state changes across components, and invoke domain services to perform business operations.

Flow concepts:

- flows act as handlers for user and system interactions (e.g. button clicks, page entry, form submission)
- flows orchestrate application behavior, calling services and updating component state
- flows coordinate multiple components and stores as part of a single interaction
- flows determine navigation and control flow between layouts or pages
- flows own error handling and recovery logic for the interactions they manage
- flows may contain light business rules, but core domain logic should live in services

For example, a login flow might call an authentication service, evaluate the result, store relevant session data, and update one or more components to reflect the outcome.

When multiple flows share orchestration resources—such as access to the same components, stores, or helper logic—it is recommended to introduce a shared base flow to centralize this responsibility and avoid duplication.

#### Layouts

Layouts bring components together to create a multi-page application. Each layout functions as a page, rendering one or more components and defining their arrangement and rendering.

Layout concepts:

- layouts are responsible for initializing and wiring components
- layouts are responsible for the visual arrangement of components
- layouts are responsible for conditional rendering based on application state or context (for example, authorisation)
- layout shouldn't handle domain errors

For example, a layout might define multiple Streamlit columns and place components within them.

### Installation

```
pip install ststeroids
```

### Getting started

StSteroids allows you to define components, layouts, and flows, then connect everything in a `main.py` by creating a StSteroids app. See the `example` folder in this repository.

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

#### The basics

To create an application using StSteroids, follow these steps:

1. Create components – Define the individual UI elements of your application, such as dialogs, tables, or metrics, using the Component base class.
2. Create flows – Implement the business or orchestration logic that interacts with components, services, and session state.
3. Create layouts – Group and initialize components, arrange them visually. Layouts define how your pages are structured.
4. Register event handlers.
5. Create the StSteroids app – Instantiate the app, register routes for each layout, and define a default route if needed.

This sequence ensures a clear separation of concerns and keeps your app modular, testable, and easy to maintain.

#### StSteroids App and routes

Example of creating a StSteroids application.

```python
app = StSteroids()

# Register a layout as a route
app.route("dashboard").to(DashboardLayout).register()

# Set a default route (optional)
app.default_route(DashboardLayout)

# Run the app (optionally specify an entry route)
app.run()
``` 

##### API reference

`app.route(name).to(layout).register()`

Registers a route that maps the route name to a layout class.
The layout is rendered when the route becomes active.

The full route builder API is as follows.

`app.route(name).to(layout).when(callable).on_enter(flow).register()`

- `when` sets up a condition by specifying a callable. The route is only registered if the callable evaluates to True
- `on_enter` registers a flow for the on enter event. The flow is dispatched once when the route becomes active, before the layout is rendered. Note! that an `on_enter` event flow should not switch page as it will break the routing concept

`app.on_app_run_once(flow)`

Registers an `on_app_run_once` event handler flow. You can use this to have an initial flow that runs once at the start of the application. Note! that an `on_app_run_once`.

`app.default_route(layout)`

Sets a default layout to display if no route is specified.

`app.run(entry_route)`

Starts the app and navigates to entry_route if provided; otherwise, uses the default route.



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

The header attribute and set_value method are specific to this example. They illustrate how components can have instance-bound attributes and provide an explicit API for updating their state. Components should own their state and expose such methods rather than allowing external code to directly mutate their attributes.

##### API Reference

`id`

Holds the component id, is automatically added from the base component.

`visible`

Controls if the component is visible. Defaults to `True` Control using the `show` and `hide` methods.

`show()`

Sets the `visible` property of the component to `True`

`hide()`

Sets the `visible` property of the component to `False`

`create(cls, component_id: str, *args, **kwargs)`
`create(cls, component_id: str, title:str ,*args, **kwargs)` (Dialog only)
`create(cls, component_id: str, refresh_interval:str ,*args, **kwargs)` (Fragment only)

Creates a new component instance with the given `component_id` and stores it in the `ComponentStore`.  
This is typically called in layouts to initialize components. Additional arguments are passed to the component's constructor.


`get(cls, component_id: str)`

Retrieves an existing component instance from the `ComponentStore` by its `component_id`.  
`create()` must have been called first; otherwise, an error will be raised.  
This is typically used in flows that need to interact with a component after it has been initialized.

`display()`

This method needs to be implemented by the subclass. To call it in a layout, use `render()`

`render()`

Executes the display method of an instance of a component.

`register_element(element_name: str)`

Registers a Streamlit element onto the component by generating component-bound key. Use this method when setting a key for an element within the component. For more information about using keys, please refer to the official Streamlit documentation.

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

`on(event_name: str, callback: Flow)`

Registers a flow as an event handler for the given event name on the component. The flow will be dispatched when the event is triggered.

`on_refresh(self, callback: Flow)` 

Registers a flow as an event handler for the refresh event of a Fragment (Fragment only)

`trigger(event_name: str)` 

Triggers the specified event and dispatches the flow registered for it.

#### Flows

Example of defining a new flow:

```python
from ststeroids import Flow

class AddDocumentFlow(Flow):
    def __init__(self, session_store: Store):
        self.session_store = session_store

    @property
    def cp_document_table(self):
        return TableComponent.get(ComponentIDs.documents)

    def run(self, ctx: FlowContext) -> None:
        # Flow logic for adding a document
```

Now imagine your application supports multiple document-related actions (for example: add, delete, or update documents).
These actions often share the same orchestration context, such as access to the session store or a document table component.

To avoid duplicating this setup in every action flow, it is recommended to introduce a base flow that provides shared orchestration resources.

First, rename the flow above to a base flow:

```python
class DocumentActionBaseFlow(Flow):
    def __init__(self, session_store: Store):
        self.session_store = session_store

    @property
    def cp_document_table(self):
        return TableComponent.get(ComponentIDs.documents)
```

Then, create a dedicated flow for each document action:

```python
class AddDocumentFlow(DocumentActionBaseFlow):
    def run(self, ctx: FlowContext):
        # Flow logic for adding a documentd
```

In this example, AddDocumentFlow represents a single user action, while DocumentActionBaseFlow provides shared orchestration context.
This keeps flows focused, avoids duplication, and clearly separates reusable setup from action-specific logic.

##### API Reference

`run(ctx: FlowContext)`

This method must be implemented by subclasses. It contains the logic that should run when the flow is triggered.

To execute a flow, register it with an event handler. When the event occurs, the framework calls `run()`.

The `FlowContext` object provides information about the event that triggered the flow and utilities for scheduling follow-up actions.

**Attributes**

`identifier`
  Identifier of the event that triggered the flow.

`type`
  Type of event that triggered the flow.

**Methods**

`schedule(function_to_schedule, args=None, kwargs=None)`
Schedules a function to run **after the next rerun**.  
This is typically used when component state must be updated before executing additional logic.

`schedule_and_rerun(function_to_schedule, args=None, kwargs=None)`
Schedules a function to run **after the next rerun** and immediately triggers a rerun. Use schedule in combination with user interactions to avoid the `calling st.rerun() within a callback is a no-op` warning.

```python
class ApproveLabelsFlow(Flow):

    def run(self, ctx: FlowContext):
        # mark selected rows as approved
        self.table.update_rows(approved=True)

        # perform backend call after rerun
        ctx.schedule_and_rerun(self.store_labels)

    def store_labels(self):
        self.backend.store(self.table.selected_rows)
```

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

Layouts are responsible for creating and rendering components.  
They must not contain business logic, checks, or flow control.

Component creation should always happen in the layout constructor using
`Component.create(...)`.

##### Rendering a layout

A layout instance can be rendered by calling its `render()` method.

```python
my_x_layout = YourXLayout.create()
my_x_layout.render()
```

Calling `render()` on a layout is restricted to the router.

This ensures:
- a single, predictable render entry point
- consistent routing behavior
- a clear separation of concerns

Layouts describe what is rendered.  
The router decides when it is rendered.

##### API Reference

 `render()`

This method needs to be implemented by the subclass.

#### Store

A wrapper around `st.session_state` to separate states into stores.

Usage:

```python
session_store = Store.create("yourstore")
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

1.0.1

- Version bump to make sure upload to pypi works

1.0.0

Partially rewritten the framework to reduce its footprint and make object creation more intuitive. Editor and debugger support has been improved, making development smoother and more productive. The router system has also been greatly enhanced, now supporting conditional routes directly within the framework, giving you more control over navigation and layout rendering.

**Note** this version is considered to be a breaking change. Make sure to adapt your code base so that it works with this new version. A small migration guide:

- Update the `__init__` of your components to match the new style
    - component_id is no longer needed
    - the `super().__init__()` no longer needs to be called
- accessing `.state` is no longer possible, you can directly access the attributes on a component instead
- Rename `render` in your components to `display`
- Remove any `show` and `hide` methods from your components as well as the `visible` property. They are now controlled by the framework
- Use a component’s `on` method to register flows as event handlers for specific component events, typically when setting up the app. Call `trigger` on the component to emit events and dispatch the registered flows.
- In Flows use `YourComponent.get(component_id)` instead of `self.component_store.get_component(component_id)
- Remove `Router` from your Flows, use `st.switch_page` instead if you didn't already
- Move the initialization of the sidebar to layouts instead of the `main` of the app
- When rendering a component call `render` instead of `execute_render`
- When creating instances of StSteroids classes use `create` instead of calling `ClassName()`. This does not apply to the `Style` class
- The flow's `run` method can no longer take parameters. Access a components state instead to aquire the require parameters
- When calling a flow, use `dispatch()` instead of `run()`
- If you previously implemented your own logic for using the `router` class. Please consider using the new Steroids app style, by doing so you can also utilize
    - The on app run once event, for initial set up
    - The router on enter event, for initial route setup. For example refresh data before rendering the page
- There are two new component types, `Fragment` and `Dialog`, they replace the `render_as` parameter. Please update your components and render calls accordingly
- Added the `schedule` functionality that allows for scheduling a run after the first rerun.

0.1.17

- Improved execute_render method by adding an error handler
- Default refresh_interval for a fragment is now `None` to avoid unintended refreshes

0.1.16

- Improved component instance creation by making component instances a singleton

0.1.15

- Added option to delete a property from the store

0.1.14

- Improved UI peformance when working with fragments.
- Improved method naming. **Note** to update the run and render calls to `execute_run` and `exectute_render`

0.1.13

- Adds a method to set a registered element's value.
- Adds a method for rendering a component as a fragment.

0.1.12

- Makes a real Singleton of the component store.
- Fixes that an invalid route exception was thrown when an error occurred while running the layout beloning to a route, instead of throwing the real error.
- Updates the readme and the example on how to have better autocomplete.

0.1.11

Considered first stable release.

< 0.1.11

Beta releases

### Todo

* the default route can only be one of the registered routes