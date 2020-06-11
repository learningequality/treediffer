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

    modified = attrs_diff['modified']
    attributes = attrs_diff['attributes']
    assert len(modified) == 0
    for attr, val_dict in attributes.items():
        assert 'old_value' not in val_dict


def test_modify_title(sample_node):
    modified_node = copy.deepcopy(sample_node)
    modified_node['title'] = 'New title'

    attrs_diff = diff_attributes(sample_node, modified_node)
    # pprint.pprint(attrs_diff)

    modified = attrs_diff['modified']
    assert len(modified) == 1
    assert 'title' in modified

    attributes = attrs_diff['attributes']
    val_dict = attributes['title']
    assert val_dict['old_value'] == sample_node['title']
    assert val_dict['value'] == modified_node['title']



# SET-LIKE NODE ATTRIBUTES
################################################################################

def test_add_and_rm_tags(sample_node_with_tags, sample_tags_add_and_rm):
    modified_node = copy.deepcopy(sample_node_with_tags)
    modified_node['tags'] = sample_tags_add_and_rm

    attrs_diff = diff_attributes(sample_node_with_tags, modified_node)
    pprint.pprint(attrs_diff)

    modified = attrs_diff['modified']
    assert len(modified) == 1
    assert 'tags' in modified

    attributes = attrs_diff['attributes']
    val_dict = attributes['tags']
    assert val_dict['old_value'] == sample_node_with_tags['tags']
    assert val_dict['value'] == modified_node['tags']


def test_tags_reordered(sample_node_with_tags, sample_tags_reordered):
    modified_node = copy.deepcopy(sample_node_with_tags)
    modified_node['tags'] = sample_tags_reordered

    attrs_diff = diff_attributes(sample_node_with_tags, modified_node)
    pprint.pprint(attrs_diff)

    modified = attrs_diff['modified']
    assert len(modified) == 1
    assert 'tags' in modified

    attributes = attrs_diff['attributes']
    val_dict = attributes['tags']
    assert val_dict['old_value'] == sample_node_with_tags['tags']
    assert val_dict['value'] == modified_node['tags']
