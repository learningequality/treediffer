import pprint
from treediffer.diffutils import contains

# SUT
from treediffer.treediffs import diff_children



DEBUG_MODE = False


# DIFF CHILDREN
################################################################################

def test_children_noop(sample_children):
    assert len(sample_children) == 3

    diff = diff_children('p1', sample_children, 'p2', sample_children)

    nodes_deleted = diff['nodes_deleted']
    assert len(nodes_deleted) == 0

    nodes_added = diff['nodes_added']
    assert len(nodes_added) == 0


def test_children_add_and_rm(sample_children, sample_children_add_and_rm):
    assert len(sample_children) == 3
    assert len(sample_children_add_and_rm) == 5

    diff = diff_children('p1', sample_children, 'p2', sample_children_add_and_rm)

    nodes_deleted = diff['nodes_deleted']
    assert len(nodes_deleted) == 1
    assert contains(nodes_deleted, {'old_node_id': 'nid2'}, by='old_node_id')

    nodes_added = diff['nodes_added']
    assert len(nodes_added) == 3
    assert contains(nodes_added, {'node_id': 'nid4'}, by='node_id')
    assert contains(nodes_added, {'node_id': 'nid5'}, by='node_id')
    assert contains(nodes_added, {'node_id': 'nid6'}, by='node_id')

    if DEBUG_MODE:
        print('\n')
        pprint.pprint(diff)


def test_children_reorder(sample_children, sample_children_reordered):
    assert len(sample_children) == 3
    assert len(sample_children_reordered) == 3

    diff = diff_children('p1', sample_children, 'p2', sample_children_reordered)

    nodes_deleted = diff['nodes_deleted']
    assert len(nodes_deleted) == 2
    assert contains(nodes_deleted, {'old_node_id': 'nid2'}, by='old_node_id')
    assert contains(nodes_deleted, {'old_node_id': 'nid3'}, by='old_node_id')

    nodes_added = diff['nodes_added']
    assert len(nodes_added) == 2
    n2 = contains(nodes_added, {'node_id': 'nid2'}, by='node_id')
    n3 = contains(nodes_added, {'node_id': 'nid3'}, by='node_id')
    assert n2, n3
    assert n2['sort_order'] > n3['sort_order'], 'after reordering nid2 should be after nid3'

    if DEBUG_MODE:
        print('\n')
        pprint.pprint(diff)
