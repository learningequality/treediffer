import copy
import json
import pprint

# SUT
from treediffer.treediffs import diff_attributes
from treediffer.presets import diff_presets




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
    # pprint.pprint(attrs_diff)

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



# ASSESSMENT ITEMS
################################################################################

def test_assessment_items_noop(sample_node_with_assessment_items):
    modified_node = copy.deepcopy(sample_node_with_assessment_items)

    attrs_diff = diff_attributes(sample_node_with_assessment_items, modified_node)

    modified = attrs_diff['modified']
    assert len(modified) == 0


def test_add_and_rm_assessment_items(sample_node_with_assessment_items, sample_assessment_items_add_and_rm):
    assessment_itemsA = sample_node_with_assessment_items['assessment_items']
    modified_node = copy.deepcopy(sample_node_with_assessment_items)
    modified_node['assessment_items'] = sample_assessment_items_add_and_rm
    assessment_itemsB = sample_assessment_items_add_and_rm

    attrs_diff = diff_attributes(sample_node_with_assessment_items, modified_node)
    # pprint.pprint(attrs_diff)

    modified = attrs_diff['modified']
    assert len(modified) == 1
    assert 'assessment_items' in modified

    attributes = attrs_diff['attributes']
    ais_diff = attributes['assessment_items']
    assert ais_diff['old_value'] == sample_node_with_assessment_items['assessment_items']
    assert ais_diff['value'] == modified_node['assessment_items']
    assert ais_diff['added'] == [assessment_itemsB[1], assessment_itemsB[3], assessment_itemsB[4]]
    assert ais_diff['deleted'] == [assessment_itemsA[1]]
    assert len(ais_diff['modified']) == 0
    assert len(ais_diff['moved']) == 0


def test_assessment_items_reordered(sample_node_with_assessment_items, sample_assessment_items_reordered):
    modified_node = copy.deepcopy(sample_node_with_assessment_items)
    modified_node['assessment_items'] = sample_assessment_items_reordered

    attrs_diff = diff_attributes(sample_node_with_assessment_items, modified_node)
    # pprint.pprint(attrs_diff)

    modified = attrs_diff['modified']
    assert len(modified) == 1
    assert 'assessment_items' in modified

    attributes = attrs_diff['attributes']
    ais_diff = attributes['assessment_items']
    assert ais_diff['old_value'] == sample_node_with_assessment_items['assessment_items']
    assert ais_diff['value'] == modified_node['assessment_items']
    assert len(ais_diff['added']) == 0
    assert len(ais_diff['deleted']) == 0
    assert len(ais_diff['modified']) == 0
    assert len(ais_diff['moved']) == 2


def test_assessment_items_with_modifications(sample_node_with_assessment_items, sample_assessment_items_with_modifications):
    assert len(sample_node_with_assessment_items['assessment_items']) == 3
    assert len(sample_assessment_items_with_modifications) == 3
    modified_node = copy.deepcopy(sample_node_with_assessment_items)
    modified_node['assessment_items'] = sample_assessment_items_with_modifications

    attrs_diff = diff_attributes(sample_node_with_assessment_items, modified_node)
    # pprint.pprint(attrs_diff)

    modified = attrs_diff['modified']
    assert len(modified) == 1
    assert 'assessment_items' in modified

    attributes = attrs_diff['attributes']
    ais_diff = attributes['assessment_items']
    assert ais_diff['old_value'] == sample_node_with_assessment_items['assessment_items']
    assert ais_diff['value'] == modified_node['assessment_items']
    assert len(ais_diff['added']) == 0
    assert len(ais_diff['deleted']) == 0
    assert len(ais_diff['modified']) == 2
    assert len(ais_diff['moved']) == 0


def test_assessment_items_with_file_modifications(sample_node_with_assessment_items, sample_assessment_items_with_file_modifications):
    assert len(sample_node_with_assessment_items['assessment_items']) == 3
    assert len(sample_assessment_items_with_file_modifications) == 3
    modified_node = copy.deepcopy(sample_node_with_assessment_items)
    modified_node['assessment_items'] = sample_assessment_items_with_file_modifications

    attrs_diff = diff_attributes(sample_node_with_assessment_items, modified_node)
    # pprint.pprint(attrs_diff)

    modified = attrs_diff['modified']
    assert len(modified) == 1
    assert 'assessment_items' in modified

    attributes = attrs_diff['attributes']
    ais_diff = attributes['assessment_items']
    assert ais_diff['old_value'] == sample_node_with_assessment_items['assessment_items']
    assert ais_diff['value'] == modified_node['assessment_items']
    assert len(ais_diff['added']) == 0
    assert len(ais_diff['deleted']) == 0
    assert len(ais_diff['modified']) == 1
    assert len(ais_diff['moved']) == 0



# STUDIO API ASSESSMENT ITEMS
################################################################################

def test_studio_exercise_cloned_noop():
    """
    Test on some sample assessment_items obtaind from the Studio API.
    """
    node1 = json.load(open('tests/fixtures/studio/peseus_exercise_node_from_api__original.json'))
    node2 = json.load(open('tests/fixtures/studio/peseus_exercise_node_from_api__cloned.json'))

    exclude_attrs = diff_presets['studio']['exclude_attrs']
    exclude_attrs += [
        'root.node_id', # == channel_id == node_id of tree root node
        'parent',       # should be parent_id (manually adding bcs API result)',
    ]
    mapA = diff_presets['studio']['mapA']
    mapB = diff_presets['studio']['mapB']

    attrs_diff = diff_attributes(node1, node2, exclude_attrs=exclude_attrs, mapA=mapA, mapB=mapB)
    # pprint.pprint(attrs_diff, width=200)
    assert len(attrs_diff['modified']) == 0


def test_studio_exercise_cloned_and_modified():
    node1 = json.load(open('tests/fixtures/studio/peseus_exercise_node_from_api__original.json'))
    node2 = json.load(open('tests/fixtures/studio/peseus_exercise_node_from_api__cloned_and_modified.json'))

    exclude_attrs = diff_presets['studio']['exclude_attrs']
    exclude_attrs += [
        'id',
        'node_id',      # expected to be different since different trees
        'parent',       # should be parent_id (manually adding bcs API result)',
    ]
    mapA = diff_presets['studio']['mapA']
    mapB = diff_presets['studio']['mapB']

    attrs_diff = diff_attributes(node1, node2, exclude_attrs=exclude_attrs, mapA=mapA, mapB=mapB)
    # pprint.pprint(attrs_diff, width=200)
    modified = attrs_diff['modified']
    assert len(modified) == 2
    assert 'files' in modified
    assert 'description' in modified






