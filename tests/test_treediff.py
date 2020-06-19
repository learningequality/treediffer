import copy
import pprint

# SUT
from treediffer.treediffs import treediff


from test_diff_subtree import sample_tree_added


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


def test_difftree_added_simplified(sample_tree, sample_tree_added):
    pass  # see test_diff_subtree.test_diff_subtree_added


def test_difftree_added_simplified(sample_tree, sample_tree_added):
    assert len(sample_tree['children']) == 3
    assert len(sample_tree_added['children']) == 5

    simplified_diff = treediff(sample_tree, sample_tree_added, format="simplified")
    # print('\n')
    # pprint.pprint(simplified_diff, width=120)

    assert len(simplified_diff['nodes_deleted']) == 0
    assert len(simplified_diff['nodes_modified']) == 0
    assert len(simplified_diff['nodes_moved']) == 0

    nodes_added = simplified_diff['nodes_added']
    assert len(nodes_added) == 5


def test_difftree_added_restructured(sample_tree, sample_tree_added):
    assert len(sample_tree['children']) == 3
    assert len(sample_tree_added['children']) == 5
    assert len(sample_tree_added['children'][4]['children']) == 3

    restructured_diff = treediff(sample_tree, sample_tree_added, format="restructured")
    # print('\n')
    # pprint.pprint(restructured_diff, width=120)
    
    assert len(restructured_diff['nodes_deleted']) == 0
    assert len(restructured_diff['nodes_modified']) == 0
    assert len(restructured_diff['nodes_moved']) == 0

    nodes_added = restructured_diff['nodes_added']
    assert len(nodes_added) == 2




# DIFF RICECOOKER TREES
################################################################################

def test_treediff_ricecooker_noop(sample_ricecooker_tree):
    assert len(sample_ricecooker_tree['children']) == 3
    unchanged_tree = copy.deepcopy(sample_ricecooker_tree)

    raw_diff = treediff(sample_ricecooker_tree, unchanged_tree, format="raw")

    diff_keys = ['nodes_deleted', 'nodes_added', 'nodes_modified', 'nodes_moved']
    for diff_key in diff_keys:
        assert raw_diff[diff_key] == []
