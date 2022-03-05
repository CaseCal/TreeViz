import numpy as np


class DisplayScheme():

    def __init__(self, metric='gini', color_bar='white_to_green', type_to_color='all'):
        self.metric = metric
        self.type_to_color = type_to_color

        if isinstance(color_bar, ColorBar):
            self.color_bar = color_bar
        elif isinstance(color_bar, str):
            self.color_bar = ColorBar.get_bar(color_bar)
        else:
            raise TypeError('color_bar must be a ColorBar object or the name of a premade one')

    @classmethod
    def get_scheme(cls, name):
        """
        Get a premade display scheme
        """

        schemes = {
            "standard": cls()
        }
        if name not in schemes:
            raise ValueError("{} is not a recognized premade DisplayScheme".format(name))
        return schemes[name]


class ColorBar():

    def __init__(self, color1, color2):
        """
        Color Bars represent a gradient of colors
        """
        self.color_left = np.array(color1)
        self.color_right = np.array(color2)

    def get_color(self, val):
        """
        Get the corresponding color of val
        """
        mixed_color = (self.color_left * (1 - val) + self.color_right * val).astype(int)
        return "#{:02X}{:02X}{:02X}".format(*mixed_color)

    @classmethod
    def get_bar(cls, name):
        """
        Get a premade color bar
        """

        bars = {
            "white_to_green": cls([0, 0, 0], [255, 255, 255])
        }
        if name not in bars:
            raise ValueError("{} is not a recognized premade ColorBar".format(name))
        return bars[name]
