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

def test_tags_noop(sample_node_with_tags):
    modified_node = copy.deepcopy(sample_node_with_tags)

    attrs_diff = diff_attributes(sample_node_with_tags, modified_node)

    modified = attrs_diff['modified']
    assert len(modified) == 0


def test_add_and_rm_tags(sample_node_with_tags, sample_tags_add_and_rm):
    modified_node = copy.deepcopy(sample_node_with_tags)
    modified_node['tags'] = sample_tags_add_and_rm

    attrs_diff = diff_attributes(sample_node_with_tags, modified_node)
    # pprint.pprint(attrs_diff)

    modified = attrs_diff['modified']
    assert len(modified) == 1
    assert 'tags' in modified

    attributes = attrs_diff['attributes']
    tags_set_diff = attributes['tags']
    assert tags_set_diff['old_value'] == sample_node_with_tags['tags']
    assert tags_set_diff['value'] == modified_node['tags']
    assert tags_set_diff['added'] == sorted(['tag4', 'tag5', 'tag6'])
    assert tags_set_diff['deleted'] == sorted(['tag2'])


def test_tags_reordered(sample_node_with_tags, sample_tags_reordered):
    modified_node = copy.deepcopy(sample_node_with_tags)
    modified_node['tags'] = sample_tags_reordered

    attrs_diff = diff_attributes(sample_node_with_tags, modified_node)
    # pprint.pprint(attrs_diff)

    modified = attrs_diff['modified']
    assert len(modified) == 0

    attributes = attrs_diff['attributes']
    val_dict = attributes['tags']
    assert val_dict['value'] == modified_node['tags']



# FILES
################################################################################

def test_files_noop(sample_node_with_files):
    modified_node = copy.deepcopy(sample_node_with_files)

    attrs_diff = diff_attributes(sample_node_with_files, modified_node)

    modified = attrs_diff['modified']
    assert len(modified) == 0


def test_add_and_rm_files(sample_node_with_files, sample_files_add_and_rm):
    filesA = sample_node_with_files['files']
    modified_node = copy.deepcopy(sample_node_with_files)
    modified_node['files'] = sample_files_add_and_rm
    filesB = sample_files_add_and_rm

    attrs_diff = diff_attributes(sample_node_with_files, modified_node)
    pprint.pprint(attrs_diff)

    modified = attrs_diff['modified']
    assert len(modified) == 1
    assert 'files' in modified

    attributes = attrs_diff['attributes']
    files_diff = attributes['files']
    assert files_diff['old_value'] == sample_node_with_files['files']
    assert files_diff['value'] == modified_node['files']
    assert files_diff['added'] == [filesB[1], filesB[3], filesB[4]]
    assert files_diff['deleted'] == [filesA[1]]


def test_files_reordered(sample_node_with_files, sample_files_reordered):
    modified_node = copy.deepcopy(sample_node_with_files)
    modified_node['files'] = sample_files_reordered

    attrs_diff = diff_attributes(sample_node_with_files, modified_node)
    # pprint.pprint(attrs_diff)

    modified = attrs_diff['modified']
    assert len(modified) == 0

    attributes = attrs_diff['attributes']
    val_dict = attributes['files']
    assert val_dict['value'] == modified_node['files']

