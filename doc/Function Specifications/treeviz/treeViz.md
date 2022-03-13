Module src.treeviz.treeViz
==========================

Classes
-------

`TreeViz(tree_model, feature_names=None, config={}, display_scheme=None, **kwargs)`
:   TreeViz is a wrapper for an sklearn DecisionTree model that adds extra dispaly functionality. Each object is initalized with a tree model, and can make structural
    changes to it to dissplay specific characteristics. Because of this, models are always copies of the original to avoid corruption, and all methods return a new copy of a TreeViz
    
    It's recommended to include the feature names when initializing, as they are not part of the actual sklearn model.
    ```python
    from sklearn.datasets import load_breast_cancer as load_data
    from sklearn.tree import DecisionTreeClassifier
    
    from treeviz import TreeViz, DisplayScheme
    
    # Breast cancer dataset
    clf = DecisionTreeClassifier(random_state=0, min_samples_leaf=5)
    data = load_data()
    clf.fit(data.data, data.target)
    
    # TreeViz
    tv = TreeViz(clf, feature_names=data.feature_names)
    
    # Raw tree
    orig_name = 'img/original_tree.png'
    tv.write_png(orig_name)
    
    # Prune
    new_tree = tv.prune()
    ```
    
    Create a new TreeViz from an sklearn decision tree

    ### Methods

    `copy(self)`
    :   Make a deep copy of the TreeViz
        
        ## Return
        New TreeViz with same tree structure

    `prune(self)`
    :   Prune tree to remove branches where the class is the same in all children.
        
        ### RETURN
        A new TreeViz without the pruned branches

    `trace(self, samples)`
    :   Trace samples through tree and remove all unused nodes
        
        ### RETURN
        A new TreeViz without the pruned branches

    `write_png(self, filename)`
    :   Draw TreeViz as a png at filename location