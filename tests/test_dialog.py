import pytest
from unittest.mock import MagicMock, patch

from ststeroids.dialog import Dialog


class MyDialog(Dialog):
    def display(self):
        pass


@pytest.fixture
def mock_dialog():
    with patch("streamlit.dialog") as mock:
        yield mock


@pytest.fixture
def dialog_instance():
    return MyDialog.create("my_dialog", title="My Title")


def test_create_sets_title(dialog_instance):
    assert dialog_instance.title == "My Title"


def test_get_does_not_set_title(dialog_instance):
    MyDialog.get("my_dialog")
    assert dialog_instance.title == "My Title"

def test_render_calls_display_inside_dialog(dialog_instance, mock_dialog):
    # Mock display
    dialog_instance.display = MagicMock()

    # st.dialog returns a decorator that immediately calls the wrapped function
    def fake_decorator(func):
        def wrapper():
            func()

        return wrapper

    mock_dialog.side_effect = lambda title: fake_decorator

    dialog_instance.render()
    dialog_instance.display.assert_called_once()
    mock_dialog.assert_called_once_with("My Title")


def test_render_skips_if_not_visible(dialog_instance, mock_dialog):
    dialog_instance.display = MagicMock()
    dialog_instance.hide()
    dialog_instance.render()
    # display should not be called
    dialog_instance.display.assert_not_called()
    mock_dialog.assert_not_called()
