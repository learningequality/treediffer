import copy
import pprint
import pytest

from treediffer.diffutils import findby

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


# ADDED AFTER RESTRUCTURING
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
    # pprint.pprint(restructured_diff)

    assert len(restructured_diff['nodes_deleted']) == 0
    assert len(restructured_diff['nodes_modified']) == 0
    assert len(restructured_diff['nodes_moved']) == 0

    nodes_added = restructured_diff['nodes_added']
    assert len(nodes_added) == 2
    n4 = findby(nodes_added, {"node_id":'nid4'}, by="node_id")
    assert n4
    t4 = findby(nodes_added, {"node_id":'T4'}, by="node_id")
    assert len(t4['children']) == 3


# DELETED AFTER RESTRUCTURING
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
    assert len(nodes_deleted) == 1  # T3 subtree
    t3 = findby(nodes_deleted, {"old_node_id":'T3'}, by="old_node_id")
    assert len(t3['children']) == 1
    t31 = findby(t3['children'], {"old_node_id":'T31'}, by="old_node_id")
    assert len(t31['children']) == 1
    t311 = findby(t31['children'], {"old_node_id":'T311'}, by="old_node_id")
    assert len(t311['children']) == 3


# ADD AND RM AFTER RESTRUCTURING
################################################################################

from test_diff_subtree import sample_tree_add_and_rm

def test_difftree_add_and_rm_restructured(sample_tree, sample_tree_add_and_rm):
    assert len(sample_tree['children']) == 3
    assert len(sample_tree_add_and_rm['children']) == 3

    diff = treediff(sample_tree, sample_tree_add_and_rm, format="restructured")
    # pprint.pprint(diff, width=120)

    nodes_deleted = diff['nodes_deleted']
    assert len(nodes_deleted) == 3

    nodes_added = diff['nodes_added']
    assert len(nodes_added) == 9

    assert len(diff['nodes_moved']) == 0
    assert len(diff['nodes_modified']) == 0



# MOVES
################################################################################

@pytest.fixture
def sample_tree_with_moves(sample_tree):
    assert len(sample_tree['children']) == 3
    modified_tree = copy.deepcopy(sample_tree)
    t1 = modified_tree['children'][0]
    t2 = modified_tree['children'][1]
    t3 = modified_tree['children'][2]

    # move T1_nid3 to be child of Topic 3
    n3 = t1['children'][2]
    assert n3['node_id'] == "T1_nid3"
    t1['children'] =  [t1['children'][0], t1['children'][1]]
    # n2['sort_order'] = t3['children'][-1]['sort_order'] + 1
    n3['node_id'] += '__new'
    t3['children'].append(n3)

    # move Subtopic 23 to be child of Topic 31
    t23 = t2['children'][2]
    t23['node_id'] += '__new'
    t2['children'] =  [t2['children'][0], t2['children'][1]]
    t31 = t3['children'][0]
    # t22['sort_order'] = t31['children'][-1]['sort_order'] + 1
    t31['children'].append(t23)

    return modified_tree


def test_treediff_with_moves_simplified(sample_tree, sample_tree_with_moves):
    assert len(sample_tree['children']) == 3
    assert len(sample_tree_with_moves['children']) == 3

    simplified_diff = treediff(sample_tree, sample_tree_with_moves, format="simplified")
    # pprint.pprint(simplified_diff)

    assert len(simplified_diff['nodes_added']) == 0
    assert len(simplified_diff['nodes_modified']) == 0
    assert len(simplified_diff['nodes_deleted']) == 0

    nodes_moved = simplified_diff['nodes_moved']
    assert len(nodes_moved) == 5


def test_treediff_with_moves_restructured(sample_tree, sample_tree_with_moves):
    assert len(sample_tree['children']) == 3
    assert len(sample_tree_with_moves['children']) == 3

    restructured_diff = treediff(sample_tree, sample_tree_with_moves, format="restructured")
    # pprint.pprint(restructured_diff)

    assert len(restructured_diff['nodes_added']) == 0
    assert len(restructured_diff['nodes_modified']) == 0
    assert len(restructured_diff['nodes_deleted']) == 0

    nodes_moved = restructured_diff['nodes_moved']
    assert len(nodes_moved) == 2



# MOVES INVOLVING REOERDERING
################################################################################

@pytest.fixture
def sample_tree_with_moves_and_reorder(sample_tree):
    """
    Same as sample_tree_with_moves but moves that also cause sort_order changes.
    """
    assert len(sample_tree['children']) == 3
    modified_tree = copy.deepcopy(sample_tree)
    t1 = modified_tree['children'][0]
    t2 = modified_tree['children'][1]
    t3 = modified_tree['children'][2]

    # move T1_nid2 to be child of Topic 3
    n2 = t1['children'][1]
    assert n2['node_id'] == "T1_nid2"
    t1['children'] =  [t1['children'][0], t1['children'][2]]
    # n2['sort_order'] = t3['children'][-1]['sort_order'] + 1
    n2['node_id'] += '__new'
    t3['children'].append(n2)

    # move Subtopic 22 to be child of Topic 31
    t22 = t2['children'][1]
    t22['node_id'] += '__new'
    t2['children'] =  [t2['children'][0], t2['children'][2]]
    t31 = t3['children'][0]
    # t22['sort_order'] = t31['children'][-1]['sort_order'] + 1
    t31['children'].append(t22)

    return modified_tree


def test_treediff_with_moves_and_reorder_simplified(sample_tree, sample_tree_with_moves_and_reorder):
    assert len(sample_tree['children']) == 3
    assert len(sample_tree_with_moves_and_reorder['children']) == 3

    simplified_diff = treediff(sample_tree, sample_tree_with_moves_and_reorder, format="simplified")
    # pprint.pprint(simplified_diff)

    assert len(simplified_diff['nodes_added']) == 0
    assert len(simplified_diff['nodes_modified']) == 0
    assert len(simplified_diff['nodes_deleted']) == 0

    nodes_moved = simplified_diff['nodes_moved']
    assert len(nodes_moved) == 5


def test_treediff_with_moves_restructured(sample_tree, sample_tree_with_moves_and_reorder):
    assert len(sample_tree['children']) == 3
    assert len(sample_tree_with_moves_and_reorder['children']) == 3

    restructured_diff = treediff(sample_tree, sample_tree_with_moves_and_reorder, format="restructured")
    # pprint.pprint(restructured_diff)

    assert len(restructured_diff['nodes_added']) == 0
    assert len(restructured_diff['nodes_modified']) == 0
    assert len(restructured_diff['nodes_deleted']) == 0

    nodes_moved = restructured_diff['nodes_moved']
    assert len(nodes_moved) == 2



# DIFF RICECOOKER TREES
################################################################################

def test_treediff_ricecooker_noop(sample_ricecooker_tree):
    assert len(sample_ricecooker_tree['children']) == 3
    unchanged_tree = copy.deepcopy(sample_ricecooker_tree)

    raw_diff = treediff(sample_ricecooker_tree, unchanged_tree, format="raw")

    diff_keys = ['nodes_deleted', 'nodes_added', 'nodes_modified', 'nodes_moved']
    for diff_key in diff_keys:
        assert raw_diff[diff_key] == []
