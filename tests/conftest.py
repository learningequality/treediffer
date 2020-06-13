import pytest
import copy

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
def sample_children_add_and_rm(sample_children):
    return [
        sample_children[0],
        {
            "node_id": "nid4",
            "content_id": "cid4",
            "title": "Fourth node",
            "description": "This node was added in the second position.",
        },
        sample_children[2],
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
def sample_children_with_modifications(sample_children):
    new_node2 = copy.deepcopy(sample_children[1])
    new_node2['title'] = "Second node (modified)"
    new_node3 = copy.deepcopy(sample_children[2])
    new_node3['description'] = "The modified descr. of the third node."
    return [
        sample_children[0],
        new_node2,
        new_node3,
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
        "files": [],
        "tags": [],
    }



# SET-LIKE FIXTURES
################################################################################

@pytest.fixture
def sample_tags():
    return ["tag1", "tag2", "tag3"]

@pytest.fixture
def sample_tags_add_and_rm():
    return ["tag1","tag4", "tag3", "tag5", "tag6"]

@pytest.fixture
def sample_tags_reordered():
    return ["tag1","tag3", "tag2"]

@pytest.fixture
def sample_node_with_tags(sample_node, sample_tags):
    node = sample_node
    node["tags"] = sample_tags
    return node



# FILES FIXTURES
################################################################################

@pytest.fixture
def sample_files():
    return [
        {
            "filename": "md5(file1.content).ext",
            "size": 1001,
            "preset": "file1_preset",
            "original_filename": "orginal_name_of_file1.ext",
            "language": "en",
            "source_url": "http://src.org/file1.ext",
        },
        {
            "filename": "md5(file2.content).ext",
            "size": 1002,
            "preset": "file2_preset",
            "original_filename": "orginal_name_of_file2.ext",
            "language": "en",
            "source_url": "http://src.org/file2.ext",
        },
        {
            "filename": "md5(file3.content).ext",
            "size": 1003,
            "preset": "file3_preset",
            "original_filename": "orginal_name_of_file3.ext",
            "language": "en",
            "source_url": "http://src.org/file3.ext",
        },
    ]

@pytest.fixture
def sample_files_add_and_rm(sample_files):
    return [
        sample_files[0],
        {
            "filename": "md5(file4.content).ext",
            "size": 1004,
            "preset": "file4_preset",
            "original_filename": "orginal_name_of_file4.ext",
            "language": "en",
            "source_url": "http://src.org/file4.ext",
        },
        sample_files[2],
        {
            "filename": "md5(file5.content).ext",
            "size": 1005,
            "preset": "file5_preset",
            "original_filename": "orginal_name_of_file5.ext",
            "language": "en",
            "source_url": "http://src.org/file4.ext",
        },
        {
            "filename": "md5(file6.content).ext",
            "size": 1006,
            "preset": "file6_preset",
            "original_filename": "orginal_name_of_file6.ext",
            "language": "en",
            "source_url": "http://src.org/file6.ext",
        },
    ]

@pytest.fixture
def sample_files_reordered(sample_files):
    return [
        sample_files[0],
        sample_files[2],
        sample_files[1],
    ]

@pytest.fixture
def sample_node_with_files(sample_node, sample_files):
    node = sample_node
    node["files"] = sample_files
    return node



# ASSESSMENT ITEMS FIXTURES
################################################################################

@pytest.fixture
def sample_assessment_items():
    return [
        {
            "assessment_id": "aid1",
            "type": "single_selection",
            "files": [
                {
                    "filename": "md5(file1.content).ext",
                    "size": 1001,
                    "preset": "file1_preset",
                    "original_filename": "orginal_name_of_file1.ext",
                    "language": "en",
                    "source_url": "http://src.org/file1.ext",
                },
                {
                    "filename": "md5(file2.content).ext",
                    "size": 1002,
                    "preset": "file2_preset",
                    "original_filename": "orginal_name_of_file2.ext",
                    "language": "en",
                    "source_url": "http://src.org/file2.ext",
                },
            ],
            "question": "Question one",
            "hints": ["q1hint1", "q1hint2"],
            "answers": ["q1ansewer1", "q1answer2"],
        },
        {
            "assessment_id": "aid2",
            "type": "multiple_selection",
            "files": [],
            "question": "Question two",
            "hints": ["q2hint1", "q2hint2"],
            "answers": ["q2ansewer1", "q2answer2"],
        },
        {
            "assessment_id": "aid3",
            "type": "single_selection",
            "files": [],
            "question": "Question three",
            "hints": ["q3hint1", "q3hint2"],
            "answers": ["q3ansewer1", "q3answer2"],
        },
    ]


@pytest.fixture
def sample_assessment_items_add_and_rm(sample_assessment_items):
    return [
        sample_assessment_items[0],
        {
            "assessment_id": "aid4",
            "type": "input_question",
            "files": [],
            "question": "Question four",
            "hints": ["q4hint1", "q4hint2"],
            "answers": ["42"],
        },
        sample_assessment_items[2],
        {
            "assessment_id": "aid5",
            "type": "single_selection",
            "files": [],
            "question": "Question five",
            "hints": ["q5hint1", "q5hint2"],
            "answers": ["q5ansewer1", "q5answer2"],
        },
        {
            "assessment_id": "aid6",
            "type": "single_selection",
            "files": [],
            "question": "Question six",
            "hints": ["q6hint1", "q6hint2"],
            "answers": ["q6ansewer1", "q6answer2"],
        },
    ]


@pytest.fixture
def sample_assessment_items_reordered(sample_assessment_items):
    return [
        sample_assessment_items[0],
        sample_assessment_items[2],
        sample_assessment_items[1],
    ]

@pytest.fixture
def sample_assessment_items_with_modifications(sample_assessment_items):
    new_ai2 = copy.deepcopy(sample_assessment_items[1])
    new_ai2['question'] = "Modified question 2"
    new_ai3 = copy.deepcopy(sample_assessment_items[2])
    new_ai3['hints'] = ["q3hint1", "q3newhint"]
    return [
        sample_assessment_items[0],
        new_ai2,
        new_ai3,
    ]

@pytest.fixture
def sample_assessment_items_with_file_modifications(sample_assessment_items):
    new_ai1 = copy.deepcopy(sample_assessment_items[0])
    new_ai1['files'] = [
        {
            "filename": "md5(file1.content).ext",
            "size": 1001,
            "preset": "file1_preset",
            "original_filename": "orginal_name_of_file1.ext",
            "language": "en",
            "source_url": "http://src.org/file1.ext",
        },
        {
            "filename": "md5(file4.content).ext",
            "size": 1004,
            "preset": "file4_preset",
            "original_filename": "orginal_name_of_file4.ext",
            "language": "en",
            "source_url": "http://src.org/file4.ext",
        },
    ]
    return [
        new_ai1,
        sample_assessment_items[1],
        sample_assessment_items[2],
    ]


@pytest.fixture
def sample_node_with_assessment_items(sample_node, sample_assessment_items):
    node = sample_node
    node["assessment_items"] = sample_assessment_items
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

