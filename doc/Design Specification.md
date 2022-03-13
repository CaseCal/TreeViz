# Motivation

This project was motivated by the need to customize the presenation of Decision Trees. Trees are not the most popular models currently, but they still have many use cases. Specifically, they are a very explainable non-parametric model, especially when explaining individual decisions. The ability to create better visuals for non-technical users is key to taking advantage of this trait.

# Intended Users

This is designed with the data scientist in mind, who must present a model to a non-technical audience. Thus, the interface allows for some complexity We assume the user is

- Familiar with sklearn and python.
- Able to write their own methods to add customization
- Usually has a specific presentation in mind, rather than exploration

On the other hand, the output is intended to generally be consumed by non-technical users. The visualizations produced should help in

- Explaining decisions
- Demonstrating logical structures
- Visualizing areas of uncertainty

# Design Considerations

## Structure vs Display

There are two fundamental types of changes made to trees. Structural changes involve adjsuting the actual nodes, while display only impacts the visualization. To keep the difference clear, structure is only changed by creating new instances, while display features are treated as settings, that have no impact when changed and only matter when an image is printed.

### Structure

Structural changes alter the shape of the tree, such as pruning nodes whose children are all the same output. Actions like this are generally irreversible, so we do a few things to try to avoid losing data.

- TreeViz as a class, that contains the underlying tree. Each different structure of a tree should be a different object. The underlying tree structure is never changed once the instance is created.
- All structural changes make a copy of the parent object. This allows for chaining and prevents sideeffects.
- Strctural changes are made to the DecisionTree model, to preserve functionality liek predict and decision_path.

For example, pruning and then tracing a decision looks like this.

```python
tv = TreeViz(clf)
new_tv = tv.prune().trace(decisions)
```

After this, tv remains unchanged, and new_tv is a new instance that has been pruned and traced.

### Display

Display does not change the shape of the tree, just the appearance of images. Display traits include colors, shading and the text within nodes. Display changes are generally very reversable, and actually have no impact until an image is actually printed. This gives a few features:

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

## Composition

TreeViz is a composition of a few underlying objects for the most part, and does not inherit any of them. This makes it a bit heavy, it can contain two large trees in different formats, but inheritance didn't really add any capabilities in either case, and both objects are necessary to retain access to.

### sklearn DecisionTree

TreeViz only works with sklearn DecisionTree models, after they are fit. It's intended to be a visualization tool, so all of the training and evaluating are expected to be done with with sklearn. So the initializaton requires an sklearn DecisonTree, and it actually retains this tree within the instance.

One reasion we need to keep the tree is to allow decisions to be evaluated. By keeping the DecisionTree, the interface is smaller because we can use some of its functionality like decision_path. Then to trace a tree, we only need the sample-array

```
clf = DecisionTreeClassifier().fit(data, target)
tv = TreeViz(clf)
X = get_new_sample() # Some new samples to trace the path of
tv.trace(X)
```

Without it, we would need to get the output directly from the original model anyways

```
clf = DecisionTreeClassifier().fit(data, target)
tv = TreeViz(clf)
X = get_new_sample() # Some new samples to trace the path of
indicator = clf.decision_path(X)
tv.trace(indicator)
```

This second method ends up being more tightly coupled, since it needs a specific sparse matrix that is aligned to the original tree. It would also prevent chaining a trace after any other change, since the original tree would no longer have the same node shape as the TreeViz instance. So for simplicity, a copy of the whole classifier is included in the TreeViz object.

### pydotplus Graph

The GraphViz object is what is acctually displayed, but is not maintained as a part of the TreeViz object. It is instead re-generated on every call to write. There are a few reasons for this:

- All structure is adjsuted in the sklearn Tree, so the DOT data is not needed.
- This ensures we do not need to worry about keeping the tree and the graph in sync when changes are made.
- Reduces the size of the TreeViz objects.
- Reduces amount of computing in most use cases, since now chaining will not contain repeat calls to create or alter the DOT data.

# <a name='Comparison'></a> Comparison to Matplotlib

## GraphViz

The largest difference is that TreeViz requires GraphViz to operate, while Matplotlib does not. GraphViz offers a much finer grained control over display, but comes at the cost of requiring a sometimes difficult install of a third-party software. Matplotlib is much more limited, but has the benefit of being a pure python library with no extra installs needed.

## Interface

_Note: Some examples in this section are not implemented yet_

### Initialization

The initialization is very similar between TreeViz and Matplotlib. Both require the model, and optionally need the feature_names and class names.

The primary difference is that Matplotlib requires the extra fig level of abstraction, and the actual function returns annotations to the graph, where TreeViz is a self-contained object.

Matplotlib

```python
fig = plt.figure(figsize=(25,20))
_ = tree.plot_tree(clf,
                   feature_names=iris.feature_names,
                   class_names=iris.target_names
                )
```

TreeViz

```python
tv = TreeViz(clf,
             feature_names=iris.feature_names,
             class_names=iris.target_names
            )
```

### Printing

Both methods write images very easily, with `savefig(filename)` for matplotlib and `write_png(filename)` for Treeviz. Treeviz does have a different method for different file types, while matplotlib uses an argument. This is because TreeViz uses the underlying pydotplus to create images, and pydotplus has separate methods. This allows for format-specific arguments, which Matplotlib does not have.

### Customization

The Matplotlib visualization is created on initialization, so all customization options have to occur during this stage. This limits it to a [relatively small list of options](https://scikit-learn.org/stable/modules/generated/sklearn.tree.plot_tree.html).

TreeViz does customization through calling structure methods and applying DisplaySchemes. This allows options to be added after initialization, which is slightly more verbose but opens up a much deeper and more natural interface.

For example, to hide the impurity:

Matplotlib

```python
fig = plt.figure(figsize=(25,20))
_ = tree.plot_tree( clf,
                    feature_names=iris.feature_names,
                    class_names=iris.target_names,
                    impurity=False,
                   )
```

TreeViz with prebuilt scheme

```python
tv = TreeViz(clf,
             feature_names=iris.feature_names,
             class_names=iris.target_names
            )
tv.display_scheme = DisplayScheme.get_scheme('simple')
```

TreeViz with custom scheme

```python
tv = TreeViz(clf,
             feature_names=iris.feature_names,
             class_names=iris.target_names
            )
scheme = DisplayScheme(metric='None')
tv.display_scheme = scheme
```

## Capability

While TreeViz has some minor interface streamlining compared to Matplotlib, the largest differentiator is in the increased capability.

Matplotlib currently has the options to:

- Show the impurity in all, only root, or none of the nodes
- Paint the nodes with default colors, and always based off majority class for classification, extremity of values for regression, or purity of node for multi-output.
- Show samples and values to be proprtions instead of absolute numbers

TreeViz has all of the above capability currently or in the next planned patch, in addition to:

- Prune a tree to only show branches that contain multiple outputs
- Trace a set of samples through a tree and:
  - Remove nodes that are not visited, or
  - Color based on sample paths
- Color based on impurity, sample size, class, or custom metrics
- Use custom colors with any of the above functionalities
- Add custom labels to nodes

For example, consider the case where an analyst wants to color a tree based on class to match some other visualizations.

In TreeViz:

```python
tv = TreeViz(clf,
             feature_names=iris.feature_names,
             class_names=iris.target_names
            )
scheme = DisplayScheme(metric='Class', color_bar='red_to_blue')
tv.display_scheme = scheme
```

In Matplotlib (Taken from [stackoverflow](https://stackoverflow.com/questions/70437840/how-to-change-colors-for-decision-tree-plot-using-sklearn-plot-tree)):

```python
colors = ['crimson', 'dodgerblue']
artists = tree.plot_tree(clf, feature_names=["X", "y"], class_names=colors,
                         filled=True, rounded=True, ax=ax2)
for artist, impurity, value in zip(artists, clf.tree_.impurity, clf.tree_.value):
    # let the max value decide the color; whiten the color depending on impurity (gini)
    r, g, b = to_rgb(colors[np.argmax(value)])
    f = impurity * 2 # for N colors: f = impurity * N/(N-1) if N>1 else 0
    artist.get_bbox_patch().set_facecolor((f + (1-f)*r, f + (1-f)*g, f + (1-f)*b))
    artist.get_bbox_patch().set_edgecolor('black')
```

# Extensability

TreeViz was designed to have great extensibility in terms of display customization. This comes at the cost of input flexibility.

## Inputs

TreeViz currently only accepts sklearn DecisionTrees. Extending to other formats would present some difficulty. For those that have a built-in way of converting to DOT data, the DisplayScheme functionality would naturally work, but all of the structural changes would likely need to be overridden, as they currently worked based on the sklearn method of storing the tree.

Anything that does not convert to DOT data will be very difficuly to include, as it will require either a manual conversion to DOT data or a bespoke DisplayScheme sub-class.

## Options

### Structure

Structural changes can be added depending on the ease of calculation. They are all done on the sklearn tree object, so that is the limiting factor on what is possible. There is currently no public interface for adjusting these, so customization will need to come from a subclass or request.

### Display

This is the most extensible part of TreeViz. Both the metric and colorbar are already set up to be extensible and customizable through public interfaces, it only requires passing in a custom function.

It is also easy to expand the pre-built options, and in fact some of them could be converted into generators for ease. For example, there are currently 'red*to_blue', 'green_to_blue' etc. prenamed colorbars. It would be easy to make a generator to allow any `<color1>\_to*<color2>` style name out of a list of standard colors.

The labels are also customizable, allowing any function to take in the labels as a dict and return any dict of new labels. The major limitation here is that the conversion must only require data from the individual node, there's not currently a way to access tree-level data. This could be possible to add but will require more work.

# ToDo List

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
