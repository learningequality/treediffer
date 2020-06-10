import pprint

from treediffer.treediffs import treediff, diff_lists
from treediffer.diffutils import contains


DEBUG_MODE = True


def test_basic_treediff():
    diff_dict = treediff({},{})
    assert diff_dict is None


def test_list_add_and_rm(sample_children, sample_children_add_and_rm):
    assert len(sample_children) == 3
    assert len(sample_children_add_and_rm) == 5

    diff = diff_lists(sample_children, sample_children_add_and_rm, 'p1', 'p2', mapA={}, mapB={}, recursive=True)

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
