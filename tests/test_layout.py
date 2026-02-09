import pytest
from ststeroids.layout import Layout
from unittest.mock import MagicMock


def test_layout_cannot_instantiate_directly():
    # Abstract classes cannot be instantiated
    with pytest.raises(TypeError):
        Layout()


def test_subclass_render_called():
    class MyLayout(Layout):
        def render(self):
            return "rendered"

    layout = MyLayout()
    layout.render = MagicMock(return_value="rendered")
    result = layout.render()
    layout.render.assert_called_once()
    assert result == "rendered"


def test_layout_create_classmethod():
    class MyLayout(Layout):
        def render(self):
            return "ok"

    layout = MyLayout.create()
    assert isinstance(layout, MyLayout)
    assert layout.render() == "ok"
