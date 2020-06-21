import copy
import pprint

# SUT
from treediffer.treediffs import treediff




DEBUG_MODE = True



# HIGH LEVEL API
################################################################################

def test_treediff_noop(sample_tree):
    assert len(sample_tree['children']) == 3
    unchanged_tree = copy.deepcopy(sample_tree)

    raw_diff = treediff(sample_tree, unchanged_tree, format="raw")

    diff_keys = ['nodes_deleted', 'nodes_added', 'nodes_modified', 'nodes_moved']
    for diff_key in diff_keys:
        assert raw_diff[diff_key] == []

def test_treediff_noop_simplified(sample_tree):
    assert len(sample_tree['children']) == 3
    unchanged_tree = copy.deepcopy(sample_tree)

    simplified_diff = treediff(sample_tree, unchanged_tree, format="simplified")
    # pprint.pprint(simplified_diff)

    diff_keys = ['nodes_deleted', 'nodes_added', 'nodes_modified', 'nodes_moved']
    for diff_key in diff_keys:
        assert simplified_diff[diff_key] == []


# ADDED
################################################################################

from test_diff_subtree import sample_tree_added


def test_difftree_added_raw(sample_tree, sample_tree_added):
    pass  # see test_diff_subtree.test_diff_subtree_added


def test_difftree_added_simplified(sample_tree, sample_tree_added):
    pass # see test_diff_subtree.test_diff_subtree_added

def test_difftree_added_restructured(sample_tree, sample_tree_added):
    assert len(sample_tree['children']) == 3
    assert len(sample_tree_added['children']) == 5
    assert len(sample_tree_added['children'][4]['children']) == 3

    restructured_diff = treediff(sample_tree, sample_tree_added, format="restructured")

    assert len(restructured_diff['nodes_deleted']) == 0
    assert len(restructured_diff['nodes_modified']) == 0
    assert len(restructured_diff['nodes_moved']) == 0

    nodes_added = restructured_diff['nodes_added']
    assert len(nodes_added) == 2
    assert len(nodes_added[1]['children']) == 3


# DELETED
################################################################################

from test_diff_subtree import sample_tree_with_removals

def test_difftree_removal_raw(sample_tree, sample_tree_with_removals):
    pass  # see test_diff_subtree.test_diff_subtree_removal


def test_difftree_removal_simplified(sample_tree, sample_tree_with_removals):
    pass  # see test_diff_subtree.test_diff_subtree_removal


def test_difftree_removal_restructured(sample_tree, sample_tree_with_removals):
    assert len(sample_tree['children']) == 3
    assert len(sample_tree_with_removals['children']) == 2

    simplified_diff = treediff(sample_tree, sample_tree_with_removals, format="restructured")

    assert len(simplified_diff['nodes_added']) == 0
    assert len(simplified_diff['nodes_modified']) == 0
    assert len(simplified_diff['nodes_moved']) == 0

    nodes_deleted = simplified_diff['nodes_deleted']
    assert len(nodes_deleted) == 1          # T3
    diff_node = nodes_deleted[0]
    assert len(diff_node['children']) == 1  # T31
    assert len(diff_node['children'][0]['children']) == 1  # T311
    assert len(diff_node['children'][0]['children'][0]['children']) == 3
    



# DIFF RICECOOKER TREES
################################################################################

def test_treediff_ricecooker_noop(sample_ricecooker_tree):
    assert len(sample_ricecooker_tree['children']) == 3
    unchanged_tree = copy.deepcopy(sample_ricecooker_tree)

    raw_diff = treediff(sample_ricecooker_tree, unchanged_tree, format="raw")

    diff_keys = ['nodes_deleted', 'nodes_added', 'nodes_modified', 'nodes_moved']
    for diff_key in diff_keys:
        assert raw_diff[diff_key] == []
