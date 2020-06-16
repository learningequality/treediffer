import copy
import pprint
from treediffer.diffutils import contains, findby

# SUT
from treediffer.treediffs import diff_subtree



DEBUG_MODE = True


# DIFF SUBTREE
################################################################################

def test_children_noop(sample_tree):
    assert len(sample_tree['children']) == 3
    unchanged_tree = copy.deepcopy(sample_tree)

    diff = diff_subtree('pA', sample_tree, 'pB', unchanged_tree)

    print('\n')
    pprint.pprint(diff, width=120)
