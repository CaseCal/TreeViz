import numpy as np


class DisplayScheme():
    """
    DisplayScheme does not change the shape of the tree, just the appearance of images. DisplayScheme traits include colors, shading and the text within nodes. DisplayScheme changes are generally very reversable, and actually have no impact until an image is actually printed. This gives a few features:

    - Changing the display of a TreeViz instance does not create a new one. DisplayScheme funcs return None to make this clear.
    - DisplayScheme settings that involve calculations (such as computing gradient from gini) are always done lazily. They will not calcualte until the image is printed.
    - DisplayScheme settings change the pydotplus Graph object, due to the higher flexibility.

    For example, to create multiple version witha different color palette

    ```python
    tv = TreeViz(clf)
    tv.set_color(palette= 'red')
    tv.write_png('red.png')
    tv.set_color(gradient=my_green_gradient)
    tv.set_color(gradient=my_blue_gradient)
    tv.write_png('blue.png')
    ```

    In the above example, there is only ever one instance of TreeViz. In addition, the gradient custom function my_green_gradient will never be called, because the tree image is not printed while that setting is active.

    """

    def __init__(self, metric='gini', color_bar='white_to_green'):
        """
        Creates a DisplayScheme with given metric and colorbar.

        * metric: String reppresenting the metric to use to color nodes.
        * color_bar: ColorBar object or name of pre-built one, determines how to convert the value produced by metric into a color.

        ## Return
        DisplayScheme
        """
        self.metric = metric

        if isinstance(color_bar, ColorBar):
            self.color_bar = color_bar
        elif isinstance(color_bar, str):
            self.color_bar = ColorBar.get_bar(color_bar)
        else:
            raise TypeError('color_bar must be a ColorBar object or the name of a premade one')

        # Specific trackers
        self._temp_state = {}

    def color_graph(self, graph):
        """
        Colors graph according to current metric and colorbar.
        """
        # Traverse nodes
        for node in graph.get_node_list():
            label = node.get_attributes().get('label')

            # Skip hidden nodes
            if label is None:
                continue

            # Adjust labels
            labels = self._parse_labels(label[1:-1])
            labels = self._compute_labels(labels)
            node.set('label', '<' + '<br/>'.join(
                "{} = {}".format(k, v).replace(" = None", '') for k, v in labels.items()
            ) + '>')

            # Record
            if 'samples' in labels and "samples" not in self._temp_state:
                self._temp_state['samples'] = int(labels['samples'])

            # Set color
            color_val = self._get_color_value(labels)
            if color_val is None:
                node.set_fillcolor('white')
            else:
                node.set_fillcolor(self.color_bar.get_color(color_val))

        # Reset state
        self._temp_state = {}

    def _compute_labels(self, labels):

        return labels

    def _get_color_value(self, labels):
        if self.metric == 'gini':
            return float(labels.get('gini', 0))
        if self.metric == 'sample_size':
            return int(labels['samples']) / self._temp_state['samples']
        return None

    @classmethod
    def get_scheme(cls, name):
        """
        Get a premade display scheme

        * name: Name of the scheme, options are ['standard']

        ## Return
        Premade DisplayScheme
        """

        schemes = {
            "standard": cls()
        }
        if name not in schemes:
            raise ValueError("{} is not a recognized premade DisplayScheme".format(name))
        return schemes[name]

    @staticmethod
    def _parse_labels(labelStr):
        pairs = [row.split('=') for row in labelStr.split('<br/>')]
        result = {}
        for pair in pairs:
            if len(pair) == 2:
                result[pair[0].strip()] = pair[1].strip()
            elif len(pair) == 1:
                result[pair[0].strip()] = None
        return result


class ColorBar():

    def __init__(self, color1, color2):
        """
        Color Bars represent a gradient of colors, and convert values to a color on teh gradient. Default implementation takes a value from 0 to 1 and translates it onto the gradient.
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

        * name: Name of the color bar. Options are ['white_to_green','white_to_blue','white_to_red']

        ## Return
        Premade ColorBar
        """

        bars = {
            "white_to_green": cls([255, 255, 255], [0, 128, 0]),
            "white_to_blue": cls([255, 255, 255], [0, 0, 128]),
            "white_to_red": cls([255, 255, 255], [128, 0, 0]),
        }
        if name not in bars:
            raise ValueError("{} is not a recognized premade ColorBar".format(name))
        return bars[name]
