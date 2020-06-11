import copy
import pprint
from treediffer.diffutils import contains

# SUT
from treediffer.treediffs import diff_attributes





# NODE ATTRIBUTES DIFFS
################################################################################

def test_attributes_noop(sample_node):
    modified_node = copy.deepcopy(sample_node)

    attrs_diff = diff_attributes(sample_node, modified_node)

    changed = attrs_diff['changed']
    attributes = attrs_diff['attributes']
    assert len(changed) == 0
    for attr, val_dict in attributes.items():
        assert 'old_value' not in val_dict


def test_modify_title(sample_node):
    modified_node = copy.deepcopy(sample_node)
    modified_node['title'] = 'New title'

    attrs_diff = diff_attributes(sample_node, modified_node)

    changed = attrs_diff['changed']
    attributes = attrs_diff['attributes']
    assert len(changed) == 1
    assert 'title' in changed

    val_dict = attributes['title']
    assert val_dict['old_value'] == sample_node['title']
    assert val_dict['value'] == modified_node['title']

    # pprint.pprint(attrs_diff)
