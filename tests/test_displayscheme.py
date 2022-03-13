import pytest

from src import ColorBar, DisplayScheme


def test_colorbar():
    bar = ColorBar([0, 0, 0], [255, 255, 255])
    assert bar.get_color(0.5) == "#7F7F7F"


def test_init_smoke():
    DisplayScheme()


@pytest.mark.parametrize('scheme', ['standard'])
def test_get_scheme(scheme):
    DisplayScheme.get_scheme(scheme)
