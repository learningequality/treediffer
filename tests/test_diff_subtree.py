import copy
import pprint
import pytest

# SUT
from treediffer.treediffs import diff_subtree


from conftest import get_topic_with_children

DEBUG_MODE = True


# DIFF SUBTREE
################################################################################

def test_diff_subtree_noop(sample_tree):
    assert len(sample_tree['children']) == 3
    unchanged_tree = copy.deepcopy(sample_tree)

    diff = diff_subtree(None, sample_tree, None, unchanged_tree)

    diff_keys = ['nodes_deleted', 'nodes_added', 'nodes_modified']
    for diff_key in diff_keys:
        assert diff[diff_key] == []

    # print('\n')
    # pprint.pprint(diff, width=120)


@pytest.fixture
def sample_tree_with_removals(sample_tree):
    modified_tree = copy.deepcopy(sample_tree)
    modified_tree['children'] = modified_tree['children'][0:2]
    return modified_tree

def test_diff_subtree_removal(sample_tree, sample_tree_with_removals):
    assert len(sample_tree['children']) == 3
    assert len(sample_tree_with_removals['children']) == 2

    diff = diff_subtree(None, sample_tree, None, sample_tree_with_removals)
    # pprint.pprint(diff, width=120)

    nodes_deleted = diff['nodes_deleted']
    assert len(nodes_deleted) == 6

    nodes_added = diff['nodes_added']
    assert len(nodes_added) == 0

    nodes_modified = diff['nodes_modified']
    assert len(nodes_modified) == 0




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

    diff = diff_subtree(None, sample_tree, None, sample_tree_added)
    # print('\n')
    # pprint.pprint(diff, width=120)

    assert len(diff['nodes_deleted']) == 0
    assert len(diff['nodes_modified']) == 0

    nodes_added = diff['nodes_added']
    assert len(nodes_added) == 5


