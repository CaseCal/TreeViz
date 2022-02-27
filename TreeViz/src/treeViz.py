# Test
import json
import copy

from sklearn import tree
from sklearn.tree._tree import TREE_LEAF
import pydotplus


class TreeViz:

    try:
         _GLOBAL_CONFIG = json.load("config.json")
    except AttributeError:
         _GLOBAL_CONFIG = {}

    def __init__(self, tree_model, config={}, **kwargs):
        """
        Create a new TreeViz from an sklearn decision tree
        """
        self._tree_model = tree_model

        # Update config with global settings -> config arg -> applicable kwargs
        self._config = copy.deepcopy(TreeViz. _GLOBAL_CONFIG)
        self._config.update(config)
        self._config.update({k: v for k, v in kwargs.items() if k in self._config})

        # Generate pydotplus graph
        self._refresh_graph()

    def copy(self):
        """
        Make a deep copy of the TreeViz
        """
        tree_copy = copy.deepcopy(self._tree_model)
        return TreeViz(tree_copy, self._config)

    def prune(self):
        """
        Prune tree to remove branches where the class is the same in all children.

        ### RETURN
        A new TreeViz without the pruned branches
        """
        newTreeViz = self.copy()
        newTreeViz._prune_index(0)
        newTreeViz._refresh_graph()
        return newTreeViz

    def _is_leaf(self, index):
        """
        Check if inner tree node of id index is a leaf
        """
        inner_tree = self._tree_model.tree_
        print(index)
        print(inner_tree.children_left[index])
        print(inner_tree.children_right[index])
        print((inner_tree.children_left[index] == TREE_LEAF
                and inner_tree.children_right[index] == TREE_LEAF))
        print()
        return (inner_tree.children_left[index] == TREE_LEAF
                and inner_tree.children_right[index] == TREE_LEAF)

    def _prune_index(self, index=0):
        """
        Turns node at index to leaf if both children have the same decisions. Recursively calls
        on children if not
        """
        inner_tree = self._tree_model.tree_
        decisions = inner_tree.value.argmax(axis=2).flatten().tolist()

        if not self._is_leaf(inner_tree.children_left[index]):
            self._prune_index(inner_tree.children_left[index])
        if not self._is_leaf(inner_tree.children_right[index]):
            self._prune_index(inner_tree.children_right[index])

        # Prune children if both children are leaves now and make the same decision
        if (self._is_leaf(inner_tree.children_left[index])
                and self._is_leaf(inner_tree.children_right[index])
                and (decisions[index] == decisions[inner_tree.children_left[index]])
                and (decisions[index] == decisions[inner_tree.children_right[index]])):

            # turn node into a leaf by "unlinking" its children
            inner_tree.children_left[index] = TREE_LEAF
            inner_tree.children_right[index] = TREE_LEAF
            print("After: {},{}".format(inner_tree.children_left[index], inner_tree.children_right[index]))

    def _refresh_graph(self):
        """
        Recalculate the graph after making changes to the tree model
        """

        dot_data = tree.export_graphviz(
            self._tree_model,
            out_file=None,
            filled=True,
            rounded=True,
            special_characters=True,
        )
        self._graph = pydotplus.graph_from_dot_data(dot_data)

    def write_png(self, filename):
        """
        Draw TreeViz as a png at filename location
        """

        self._graph.write_png(filename)

    def __eq__(self, other):
        """
        Tests equality of tree._value and config
        """
        return ((self._tree_model.tree_.value == other._tree_model.tree_.value).all()
                and self._config == other._config)
