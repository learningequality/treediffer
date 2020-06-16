import copy
import pprint

# SUT
from treediffer.treediffs import diff_subtree



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

    print('\n')
    pprint.pprint(diff, width=120)