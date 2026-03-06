import pytest
from unittest.mock import MagicMock, patch

from ststeroids.fragment import Fragment
from ststeroids.flow import Flow

class MyFragment(Fragment):
    def display(self):
        pass

@pytest.fixture
def mock_fragment():
    with patch("streamlit.fragment") as mock:
        yield mock


@pytest.fixture
def fragment_instance():
    return MyFragment.create("frag1", refresh_interval="5s")


def test_create_sets_refresh_interval(fragment_instance):
    assert fragment_instance.refresh_interval == "5s"

def test_get_does_not_set_refresh_interval(fragment_instance):
    MyFragment.get("my_dialog")
    assert fragment_instance.refresh_interval == "5s"


def test_on_refresh_registers_flow(fragment_instance):
    flow = MagicMock(spec_set=Flow)
    fragment_instance.on_refresh(flow)
    assert fragment_instance._events[fragment_instance.EVENT_REFRESH] == flow


def test_render_calls_display_inside_fragment(fragment_instance, mock_fragment):
    # Mock display and trigger
    fragment_instance.display = MagicMock()
    fragment_instance.trigger = MagicMock()

    # st.fragment returns a decorator that calls the wrapped function immediately
    def fake_decorator(func):
        def wrapper():
            func()

        return wrapper

    mock_fragment.side_effect = lambda run_every=None: fake_decorator

    fragment_instance.render()

    mock_fragment.assert_called_once_with(run_every="5s")
    fragment_instance.trigger.assert_called_once_with(fragment_instance.EVENT_REFRESH)
    fragment_instance.display.assert_called_once()


def test_render_skips_if_not_visible(fragment_instance, mock_fragment):
    fragment_instance.display = MagicMock()
    fragment_instance.trigger = MagicMock()
    fragment_instance.hide()
    fragment_instance.render()
    fragment_instance.display.assert_not_called()
    fragment_instance.trigger.assert_not_called()
    mock_fragment.assert_not_called()
