# Test
import json
import copy

from sklearn import tree
from sklearn.tree._tree import TREE_LEAF
import pydotplus


class TreeViz:

    GLOBAL_CONFIG = json.load("config.json")

    def __init__(self, tree_model, config={}, **kwargs):
        """
        Create a new TreeViz from an sklearn decision tree
        """
        self._tree_model = tree_model
        self._inner_tree = tree_model.tree_
        self._decisions = tree_model.tree_.value.argmax(axis=2).flatten().tolist()

        # Update config with global settings -> config arg -> applicable kwargs
        self._config = copy.deepcopy(TreeViz.GLOBAL_CONFIG)
        self._config.update(config)
        self._config.update({k: v for k, v in kwargs.items() if k in self._config})

        # Generate pydotplus graph
        dot_data = tree.export_graphviz(
            tree_model,
            out_file=None,
            filled=True,
            rounded=True,
            special_characters=True,
        )
        self._graph = pydotplus.graph_from_dot_data(dot_data)

    def prune(self):
        """
        Prune tree to remove branches where the class is the same in all children.

        # RETURN
        A new TreeViz without the pruned branches
        """
        tree_model_copy = copy.deepcopy(self._tree_model)
        decisions = tree_model_copy.tree_.value.argmax(axis=2).flatten().tolist()
        new_tree_model = TreeViz._prune_index(tree_model_copy.tree_, decisions)
        return TreeViz(new_tree_model)

    def _is_leaf(self, index):
        """
        Check if inner tree node of id index is a leaf
        """
        return (self.inner_tree.children_left[index] == TREE_LEAF
                and self._inner_tree.children_right[index] == TREE_LEAF)

    def _prune_index(self, index=0):
        """
        Turns node at index to leaf if both children have the same decisions. Recursively calls
        on children if not
        """
        is_leaf = TreeViz._is_leaf
        prune_index = TreeViz._prune_index
        inner_tree = self._inner_tree
        decisions = self._decisions

        if not is_leaf(inner_tree, inner_tree.children_left[index]):
            prune_index(inner_tree, decisions, inner_tree.children_left[index])
        if not is_leaf(inner_tree, inner_tree.children_right[index]):
            prune_index(inner_tree, decisions, inner_tree.children_right[index])

        # Prune children if both children are leaves now and make the same decision
        if (is_leaf(inner_tree, inner_tree.children_left[index])
                and is_leaf(inner_tree, inner_tree.children_right[index])
                and (decisions[index] == decisions[inner_tree.children_left[index]])
                and (decisions[index] == decisions[inner_tree.children_right[index]])):

            # turn node into a leaf by "unlinking" its children
            inner_tree.children_left[index] = TREE_LEAF
            inner_tree.children_right[index] = TREE_LEAF
