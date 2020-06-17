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


def test_treediff_ricecooker_noop(sample_ricecooker_tree):
    assert len(sample_ricecooker_tree['children']) == 3
    unchanged_tree = copy.deepcopy(sample_ricecooker_tree)

    raw_diff = treediff(sample_ricecooker_tree, unchanged_tree, format="raw")
    
    diff_keys = ['nodes_deleted', 'nodes_added', 'nodes_modified', 'nodes_moved']
    for diff_key in diff_keys:
        assert raw_diff[diff_key] == []
