[![Build Status](https://app.travis-ci.com/CaseCal/TreeViz.svg?branch=main)](https://app.travis-ci.com/CaseCal/TreeViz)

# TreeViz

Visualization toolkit for sklearn Decision Trees using graphviz and pydotplus.

# Installation

TreeViz displays and modifies Decison Trees using [GraphViz](https://www.graphviz.org/), an open source graph visualization software. GraphViz must be installed on your machine in [a location that pydotplus searches](https://pydotplus.readthedocs.io/reference.html#pydotplus.graphviz.find_graphviz). The installation at [Anaconda](https://anaconda.org/anaconda/graphviz#:~:text=anaconda%20%2F%20packages%20%2F%20graphviz%201,Open%20Source%20graph%20visualization%20software.) is a good place to start, as it will add the GraphViz location to PATH in most scenarios.

Once GraphViz is installed, TreeViz can be installed through pip:

```
pip install -i https://test.pypi.org/simple/ treeviz
```

# Examples

See [examples folder](examples) for more examples

# Documentation

See [doc folder](doc) for:

- [Design](doc/Design%20Specification.md)
- [Function Specifications](doc/Function%20Specifications/treeviz)
- [Overview Presentation](doc/TreeViz.pptx)
- [Software Comparison](doc/Design%20Specification.md#Comparison)

# Testing

Run using

```
python -m pytest
```

# Upcoming Additions

## Output Formats

These are just boilerplate to the underlying pydotplus library.

- svg
- jpeg

## Class Names

These will need to be passed in the initialization, same as feature names are now, to dispaly in the tree

## More Metrics

The focus is on bespoke metrics that can't be replicated with the custom input, i.e those that require tree-level data

- Samples as percent of total
- Test error (Would require new samples)
- Regression values

## Colors

- ColorBar generators as mentioned above, to allow colot_to_color naming.
- Implement library (maybe matplotlib?) with color functionality to allow more than just rgb int triples.
- Add ability for non-linear coloring, such as white in middle or higher alphas at edges, etc.
