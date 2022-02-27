import pytest

from sklearn.datasets import load_iris
from sklearn.tree import DecisionTreeClassifier

from src import TreeViz


def standard_tree():
    clf = DecisionTreeClassifier(random_state=0)
    iris = load_iris()
    return clf.fit(iris.data, iris.target)


def prunable_tree():
    clf = DecisionTreeClassifier(random_state=0, min_samples_leaf=5)
    data = load_iris()
    return clf.fit(data.data, data.target)


@pytest.mark.parametrize('tree', (standard_tree(), prunable_tree()))
def test_init_smoke(tree):
    TreeViz(tree)


@pytest.mark.parametrize('tree', (standard_tree(), prunable_tree()))
def test_config(tree):
    config = {"setting_A": 1, "setting_B": True}
    tv = TreeViz(tree, config=config, setting_B=False)

    assert tv._config["setting_A"] == 1
    assert tv._config["setting_B"] is False

@pytest.mark.parametrize('tree', (standard_tree(), prunable_tree()))
def test_write_smoke(tree, tmp_path):
    tv = TreeViz(tree)
    d = tmp_path / "sub"
    d.mkdir()
    p = d / "tree.png"
    tv.write_png(str(p))

@pytest.mark.parametrize('tree', (standard_tree(), prunable_tree()))
def test_prune_no_side_effect(tree):
    tv = TreeViz(tree)
    tv_copy = tv.copy()
    tv_pruned = tv.prune()

    assert tv == tv_copy
    assert tv is not tv_pruned

@pytest.mark.parametrize('tree', (standard_tree(), prunable_tree()))
def test_prune_idempotent(tree):
    tv = TreeViz(tree)
    tv_pruned = tv.prune()
    tv_pruned_twice = tv_pruned.prune()

    assert tv_pruned == tv_pruned_twice
