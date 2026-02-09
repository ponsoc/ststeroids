import pytest
from unittest.mock import MagicMock

from ststeroids.flow import Flow


def test_flow_cannot_instantiate_directly():
    with pytest.raises(TypeError):
        Flow()


def test_subclass_run_called_by_dispatch():
    class MyFlow(Flow):
        def run(self, ctx):
            pass

    flow = MyFlow.create()
    flow.run = MagicMock()
    flow.dispatch(None)
    flow.run.assert_called_once_with(None)


def test_flow_create_classmethod():
    class MyFlow(Flow):
        def run(self, ctx):
            pass

    flow = MyFlow.create()
    assert isinstance(flow, MyFlow)
    result = flow.run(None)
    assert result is None