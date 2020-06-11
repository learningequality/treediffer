import pytest


# LIST-LIKE FIXTURES
################################################################################

@pytest.fixture
def sample_children():
    return [
        {
            "node_id": "nid1",
            "content_id": "cid1",
            "title": "First node",
            "description": "The descr. of the first node in the children.",
        },
        {
            "node_id": "nid2",
            "content_id": "cid2",
            "title": "Second node",
            "description": "The second node is very special.",
        },
        {
            "node_id": "nid3",
            "content_id": "cid3",
            "title": "Third node",
            "description": "The third node descr. is just the same thing again.",
        },
    ]

@pytest.fixture
def sample_children_add_and_rm():
    return [
        {
            "node_id": "nid1",
            "content_id": "cid1",
            "title": "First node",
            "description": "The descr. of the first node in the children.",
        },
        {
            "node_id": "nid4",
            "content_id": "cid4",
            "title": "Fourth node",
            "description": "This node was added in the second position.",
        },
        {
            "node_id": "nid3",
            "content_id": "cid3",
            "title": "Third node",
            "description": "The third node descr. is just the same thing again.",
        },
        {
            "node_id": "nid5",
            "content_id": "cid5",
            "title": "Fifth node",
            "description": "This node was added appended after the third node.",
        },
        {
            "node_id": "nid6",
            "content_id": "cid6",
            "title": "Sixth node",
            "description": "This node is last in the list.",
        },
    ]


@pytest.fixture
def sample_children_reordered(sample_children):
    return [
        sample_children[0],
        sample_children[2],
        sample_children[1],
    ]


# NODE FIXTURES
################################################################################


@pytest.fixture
def sample_node():
    return {
        "kind_id": "document",
        "node_id": "nidx",
        "content_id": "cidx",
        "title": "Sample node",
        "description": "This node is super simple.",
        "language": "en",
        "children": [],
    }



# SET-LIKE FIXTURES
################################################################################

@pytest.fixture
def sample_tags():
    return ['tag1', 'tag2', 'tag3']

@pytest.fixture
def sample_tags_add_and_rm():
    return ['tag1','tag4', 'tag3', 'tag5', 'tag6']

@pytest.fixture
def sample_tags_reordered():
    return ['tag1','tag3', 'tag2']

@pytest.fixture
def sample_node_with_tags(sample_node, sample_tags):
    node = sample_node
    node['tags'] = sample_tags
    return node



# TREE FIXTURES
################################################################################

@pytest.fixture
def basic_tree(sample_children):
    return {
        "title": "Basic tree",
        "source_id": "basic-tree",
        "description": "A simple tree we can modify for all kinds of tests",
        "language": "en",
        "children": sample_children(),
    }

