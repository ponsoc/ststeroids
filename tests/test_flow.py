import pytest
from ststeroids.flow import Flow
from ststeroids.store import ComponentStore


def test_flow_initializes_component_store():
    flow = Flow()
    assert isinstance(flow.component_store, ComponentStore)


def test_flow_run_raises_not_implemented_error():
    flow = Flow()
    with pytest.raises(NotImplementedError):
        flow.run()


def test_flow__run_raises_not_implemented_error():
    flow = Flow()
    with pytest.raises(NotImplementedError):
        flow._run()


def test_subclass_run_called_by__run():
    class MyFlow(Flow):
        def run(self, x):
            return x * 2

    flow = MyFlow()
    result = flow._run(3)
    assert result == 6