from src.treeviz import ColorBar


def test_colorbar():
    bar = ColorBar([0, 0, 0], [255, 255, 255])
    assert bar.get_color(0.5) == "#7F7F7F"
