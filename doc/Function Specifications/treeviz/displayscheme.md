Module src.treeviz.displayscheme
================================

Classes
-------

`ColorBar(color1, color2)`
:   Color Bars represent a gradient of colors, and convert values to a color on teh gradient. Default implementation takes a value from 0 to 1 and translates it onto the gradient.

    ### Static methods

    `get_bar(name)`
    :   Get a premade color bar
        
        * name: Name of the color bar. Options are ['white_to_green','white_to_blue','white_to_red']
        
        ## Return
        Premade ColorBar

    ### Methods

    `get_color(self, val)`
    :   Get the corresponding color of val

`DisplayScheme(metric='gini', color_bar='white_to_green')`
:   DisplayScheme does not change the shape of the tree, just the appearance of images. DisplayScheme traits include colors, shading and the text within nodes. DisplayScheme changes are generally very reversable, and actually have no impact until an image is actually printed. This gives a few features:
    
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
    
    Creates a DisplayScheme with given metric and colorbar.
    
    * metric: String reppresenting the metric to use to color nodes.
    * color_bar: ColorBar object or name of pre-built one, determines how to convert the value produced by metric into a color.
    
    ## Return
    DisplayScheme

    ### Static methods

    `get_scheme(name)`
    :   Get a premade display scheme
        
        * name: Name of the scheme, options are ['standard']
        
        ## Return
        Premade DisplayScheme

    ### Methods

    `color_graph(self, graph)`
    :   Colors graph according to current metric and colorbar.