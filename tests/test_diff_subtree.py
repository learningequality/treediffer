import copy
import pprint
import pytest

# SUT
from treediffer.treediffs import diff_subtree


from treediffer.diffutils import print_diff
from conftest import get_topic_with_children

DEBUG_MODE = True

# DIFF SUBTREE
################################################################################

def test_diff_subtree_noop(sample_tree):
    assert len(sample_tree['children']) == 3
    unchanged_tree = copy.deepcopy(sample_tree)

    diff = diff_subtree(None, sample_tree, None, unchanged_tree, root=True)

    diff_keys = ['nodes_deleted', 'nodes_added', 'nodes_modified']
    for diff_key in diff_keys:
        assert diff[diff_key] == []



# ADDED
################################################################################

@pytest.fixture
def sample_tree_added(sample_tree, sample_children):
    modified_tree = copy.deepcopy(sample_tree)
    sample_children_copy = copy.deepcopy(sample_children)
    t4 = get_topic_with_children('T4', sample_children_copy)
    modified_tree['children'].extend([
        {
            "node_id": "nid4",
            "content_id": "cid4",
            "title": "Newly added node",
            "description": "The descr. of the newly added node.",
        },
        t4,
    ])
    return modified_tree

def test_diff_subtree_added(sample_tree, sample_tree_added):
    assert len(sample_tree['children']) == 3
    assert len(sample_tree_added['children']) == 5

    diff = diff_subtree(None, sample_tree, None, sample_tree_added, root=True)
    # print('\n')
    # pprint.pprint(diff, width=120)

    assert len(diff['nodes_deleted']) == 0
    assert len(diff['nodes_modified']) == 0

    nodes_added = diff['nodes_added']
    assert len(nodes_added) == 5



# DELETED
################################################################################

@pytest.fixture
def sample_tree_with_removals(sample_tree):
    modified_tree = copy.deepcopy(sample_tree)
    modified_tree['children'] = modified_tree['children'][0:2]
    return modified_tree

def test_diff_subtree_removal(sample_tree, sample_tree_with_removals):
    assert len(sample_tree['children']) == 3
    assert len(sample_tree_with_removals['children']) == 2

    diff = diff_subtree(None, sample_tree, None, sample_tree_with_removals, root=True)
    # pprint.pprint(diff, width=120)
    # print_diff(diff)

    assert len(diff['nodes_added']) == 0
    assert len(diff['nodes_modified']) == 0

    nodes_deleted = diff['nodes_deleted']
    assert len(nodes_deleted) == 6


# ADD AND RM
################################################################################

@pytest.fixture
def sample_tree_add_and_rm(sample_tree, sample_children):
    modified_tree = copy.deepcopy(sample_tree)
    sample_children_copy = copy.deepcopy(sample_children)
    t1 = modified_tree['children'][0]
    t1['children'] = [
        t1['children'][0],
        {
            "node_id": "nid4",
            "content_id": "cid4",
            "title": "First newly added node",
            "description": "The descr. of the newly added node.",
        },
        t1['children'][2],
        {
            "node_id": "nid5",
            "content_id": "cid5",
            "title": "Second newly added node",
            "description": "The descr. of the newly added node.",
        },
        {
            "node_id": "nid6",
            "content_id": "cid6",
            "title": "Third newly added node",
            "description": "The descr. of the newly added node.",
        },
    ]
    t2 = modified_tree['children'][1]
    t4 = get_topic_with_children('T4', sample_children_copy)
    t5 = get_topic_with_children('T5', sample_children_copy)
    t6 = get_topic_with_children('T6', sample_children_copy)
    t2['children'] = [
        t2['children'][0],
        t4,
        t2['children'][2],
        t5,
        t6,
    ]
    t311 = modified_tree['children'][2]['children'][0]['children'][0]
    t311['children'] = [
        t311['children'][0],
        {
            "node_id": "nid3114",
            "content_id": "cid3114",
            "title": "First added node in T311",
            "description": "The descr. of the newly added node.",
        },
        t311['children'][2],
        {
            "node_id": "nid3115",
            "content_id": "cid3115",
            "title": "Second added node in T311",
            "description": "The descr. of the newly added node.",
        },
        {
            "node_id": "nid3116",
            "content_id": "cid3116",
            "title": "Third added node in T311",
            "description": "The descr. of the newly added node.",
        },
    ]
    return modified_tree

def test_diff_subtree_add_and_rm(sample_tree, sample_tree_add_and_rm):
    assert len(sample_tree['children']) == 3
    assert len(sample_tree_add_and_rm['children']) == 3

    diff = diff_subtree(None, sample_tree, None, sample_tree_add_and_rm, root=True)
    # pprint.pprint(diff, width=120)
    # print_diff(diff)

    nodes_added = diff['nodes_added']
    assert len(nodes_added) == 18
    assert len(diff['nodes_modified']) == 0
     
    nodes_deleted = diff['nodes_deleted']
    assert len(nodes_deleted) == 6
