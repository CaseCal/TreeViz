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

- Changing the display of a TreeViz instance does not create a new one. Display funcs return None to make this clear.
- Display settings that involve calculations (such as computing gradient from gini) are always done lazily. They will not calcualte until the image is printed.
- Display settings change the pydotplus Graph object, due to the higher flexibility.

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

The GraphViz object is also a component, build from the export_graphviz sklearn function and modified using pydotplus. This object represents the visual graph, and is a lot more flexible to modify than the DecisionTree. However, it's also not explicitly a tree, and so changing the structure of it can easily break the tree structure.
