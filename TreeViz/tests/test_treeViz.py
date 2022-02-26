from sklearn.datasets import load_iris
from sklearn.tree import DecisionTreeClassifier

from TreeViz import TreeViz


def get_sk_tree():
    clf = DecisionTreeClassifier(random_state=0)
    iris = load_iris()
    return clf.fit(iris.data, iris.target)


def test_init_smoke():
    TreeViz(get_sk_tree())


def test_config():
    config = {"setting_A": 1, "setting_B": True}
    tv = TreeViz(get_sk_tree(), config=config, setting_B=False)

    assert tv._config["setting_A"] == 1
    assert tv._config["setting_B"] is False


def test_prune_no_side_effect():
    tv = TreeViz(get_sk_tree())
    tv_copy = tv.copy()
    tv_pruned = tv.prune()

    assert tv == tv_copy
    assert tv is not tv_pruned


def test_prune_idempotent():
    tv = TreeViz(get_sk_tree())
    tv_pruned = tv.prune()
    tv_pruned_twice = tv_pruned.prune()

    assert tv_pruned == tv_pruned_twice
