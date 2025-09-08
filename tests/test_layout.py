import pytest
from ststeroids.layout import Layout
from unittest.mock import MagicMock


def test_layout_render_raises_not_implemented_error():
    layout = Layout()
    with pytest.raises(NotImplementedError):
        layout.render()


def test_subclass_run_called_by__run():
    class MyLayout(Layout):
        def render(self):
            return ""

    layout = MyLayout()
    layout.render = MagicMock()
    layout.execute_render()
    layout.render.assert_called_once()
