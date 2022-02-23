from sklearn.datasets import load_breast_cancer as load_data
from sklearn.tree import DecisionTreeClassifier

from TreeViz import TreeViz


# Iris dataset
clf = DecisionTreeClassifier(random_state=0, min_samples_leaf=5)
data = load_data()
clf.fit(data.data, data.target)

# TreeViz
tv = TreeViz(clf)

# Raw tree
tv.write_png("unpruned.png")

# Prune and write
tv.prune().write_png("pruned.png")