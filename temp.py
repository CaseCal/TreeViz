from sklearn.datasets import load_breast_cancer as load_data
from sklearn.tree import DecisionTreeClassifier

from src.treeviz import TreeViz, DisplayScheme
# Breast cancer dataset
clf = DecisionTreeClassifier(random_state=0, min_samples_leaf=5)
data = load_data()
clf.fit(data.data, data.target)

# TreeViz
tv = TreeViz(clf, feature_names=data.feature_names)

# Raw tree
tv.write_png("unpruned.png")

traced = tv.trace(data.data[0:2])
traced.write_png("traced.png")

# Colored
std = DisplayScheme.get_scheme('standard')
std.metric = 'sample_size'
traced.display_scheme = std
traced.write_png("traced_better_color.png")