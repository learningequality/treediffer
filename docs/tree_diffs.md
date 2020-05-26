Tree diffs
==========

The functions in `utils/tree_diffs.py` can be used to create a dict
of differences between two studio trees.


### Example of node added
A node added to the tree is appears under the key `nodes_added.{node_id}` and is
represented by the following dict:
```python
added = {
    "parent": (str),
    "node_id": (str),
    "attributes": {
        "title": "The title of the new node",
        "description": "The description of the new node",
        "content_id": (str),
        "sort_order": (float),
        ...
    }
}
```
To apply this "patch," create a new `c = ContentNode(**attributes)`, find the
parent node where the new node is to be added,
`parent_node = ContenNode.filter(tree_id=...).get(node_id=added['parent'])`,
then calling `parent_node.children.add(c)`.


### Example of node deleted
A node deletion will appears under the key `nodes_deleted.{node_id}` and the
attributes key contains the info of the node that was deleted:
```python
deleted = {
    "old_parent": (str),
    "node_id": (str),
    "attributes": {
        "title": "The title of the node to be deleted",
        "description": "The description of the node",
        "content_id": (str),
        "sort_order": (float),
        ...
    }
}
```
To apply this deletion patch, find content node
`c = ContenNode.filter(tree_id=...).get(node_id=deleted['node_id'])`, and its parent
`parent_node = ContenNode.filter(tree_id=...).get(node_id=deleted['old_parent'])`,
then call `parent_node.children.remove(c)`. The `attributes` dict is provided
for information purposes only (e.g. to display the node being deleted in the UI).


### Example of node modified
When a node appears in both the "before tree" and the "after tree" in the same
location within the tree, it will have the same `node_id`. The modifications to
the node attributes are represented using the following data structure:
```python
modified = {
    "parent": (str),
    "node_id": (str),
    "attributes": {
        "title":{
            "old_value": "Old title",
            "value": "The title of the new node"
        },
        "description": { "value": "The description of the new node" },
        "content_id": { "value": (str) },
        "sort_order": { "value": (float) },
        "tags": {
            "added": ['newtag1', 'newtag2'],
            "removed": ['deletedtag3', 'deletedtag4'],
        },
        "assessment_items": {
            "added": [
                { 'assessment_id': 'a000000000000000000000000000000e', ... }
            ]
            "removed": [] ...
        }
    }
}
```




### Example of node moved

```python
   moved = {
      "old_parent": (str),
      "old_node_id": (str),
      "parent": (str),
      "node_id": (str),
      'attributes': {}
    }
```


Here is a complete example of a diff:

```python

{
    'nodes_modified': {
        '00000000000000000000000000000001': {
          'title': 'Topic A changed'
          'tags': {'new': ['tag1']},
        },
        '00000000000000000000000000000005': {
          'assessment_items': {'added': [{
            'answers': '[{"answer": 100, "help_text": "", "correct": true}]'
                ,
            'assessment_id': 'a000000000000000000000000000000e',
            'hints': '[]',
            'order': 1,
            'question': 'Question 5?',
            'randomize': False,
            'raw_data': '',
            'source_url': None,
            'type': 'input_question',
            }], 'deleted': [{
            'answers': '[{"answer": 10, "help_text": "", "correct": true}, {"answer": 1.5, "help_text": "", "correct": true}]'
                ,
            'assessment_id': 'a000000000000000000000000000000c',
            'hints': '[]',
            'order': 1,
            'question': 'Question 3?',
            'randomize': False,
            'raw_data': '',
            'source_url': None,
            'type': 'input_question',
            }],
                'modified': [{'answers': '[{"answer": "Answer 1", "help_text": "", "correct": false}, {"answer": "Answer 2 changed", "help_text": "", "correct": true}]'
                              ,
                              'assessment_id': 'a000000000000000000000000000000b'
                              , 'hints': '[]'},
                              {'assessment_id': 'a000000000000000000000000000000a'
                              ,
                              'hints': '[{"order": 1, "hint": "Hint 1"}]'
                              , 'question': 'Question 1 changed?'}]},
                'extra_fields': {
            'm': 3,
            'mastery_model': 'm_of_n',
            'n': 5,
            'randomize': True,
            }},
        '00000000000000000000000000000006': {'files': {'modified': [{'checksum': 'ff0a3b7f3daef040faf89a88fdac01b7'
                , 'preset_id': 'high_res_video'}]}},
        '00000000000000000000000000000007': {'files': {'added': [{
            'checksum': '697e30045d911834638fb540052cf766',
            'file_format_id': 'mp4',
            'language_id': None,
            'preset_id': 'low_res_video',
            'source_url': None,
            }]}},
        '00000000000000000000000000000011': {'files': {'deleted': [{
            'checksum': 'c3fd9a7d4d433f199ac2a7f2211acf7b',
            'file_format_id': 'mp4',
            'language_id': None,
            'preset_id': 'high_res_video',
            'source_url': None,
            }]}},
        },
    'nodes_moved': {'bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb': {
        'attributes': {},
        'new_node_id': 'bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb',
        'new_parent': '00000000000000000000000000000002',
        'old_node_id': '00000000000000000000000000000003',
        'old_parent': '00000000000000000000000000000001',
        }},
    }                                               
diff = {
        "nodes_modified": [
            "<node_id (str)>": {
                "node_id": (str),
                "content_id": (str),
                "attributes": {
                    "title": {
                        "changed": (bool),
                        "old_value": (str),
                        "value": (str)
                    },
                    ...,
                    "files": ([{
                        "filename": (str),
                        "file_size": (int),
                        "preset": (str)
                    }]),
                    "assessment_items": {
                        "modified": [{...}],
                        "added": [{...}],
                        "deleted": [{...}],
                        "moved": [{...}],
                    },
                    "tags": {
                        "added": [{...}],
                        "deleted": [{...}],
                    },
                }
            },
            ...
        ],
        "nodes_added": [
            "<node_id (str)>": {
                "node_id": (str),
                "content_id": (str),
                "parent": (str),
                "attributes": {...}
            },
            ...
        ],
        "nodes_deleted": [
            "<node_id (str)>": {"old_parent": (str), "attributes": {...}},
            ...
        ],
        "nodes_moved": [
            "<node_id (str)>": {"old_parent": (str), "new_parent": (str), "attributes": {...}},
            ...
        ]
    }
```



Determining if node is added/moved/removed:

Node id captures whether or not the (parent node_id, node_id) edge exists
  - Main = # of times content id is in main tree
  - Staged = # of times content id is in staging tree
  - node_id_diff = union(Main node ids, Staged node ids) - intersection(Main node ids, Staged node ids)

```
 # Main = # Staged | # Main > # Staged       | # Main < # Staged
----------------------------------------------------------------
 All nodes in      | (# Main - # Staged)     | (# Staged - # Main)
 node_id_diff      | have been removed,      | have been added,
 have moved        |                         |
                   | (# Staged -             | (# Staged - len(node_intersection))
                   | len(node_intersection)) | have moved   
                   | have moved              | 
```


















## Old diff format (original PR):

```python
diff = {
        "nodes_modified": [
            "<node_id (str)>": {
                "attributes": {
                    "title": {
                        "changed": (bool),
                        "value": (str)
                    },
                    "files": ([{
                        "filename": (str),
                        "file_size": (int),
                        "preset": (str)
                    }]),
                    "assessment_items": ([AssessmentItem]),
                    "tags": ([Tag]),
                    ...
                }
            },
            ...
        ],
        "nodes_added": [
            "<node_id (str)>": { "new_parent": (str),  "attributes": {...}},
            ...
        ],
        "nodes_deleted": [
            "<node_id (str)>": {"old_parent": (str), "attributes": {...}},
            ...
        ],
        "nodes_moved": [
            "<node_id (str)>": {"old_parent": (str), "new_parent": (str), "attributes": {...}},
            ...
        ]
    }
```



Determining if node is added/moved/removed:

Node id captures whether or not the (parent node_id, node_id) edge exists
  - Main = # of times content id is in main tree
  - Staged = # of times content id is in staging tree
  - node_id_diff = union(Main node ids, Staged node ids) - intersection(Main node ids, Staged node ids)

```
 # Main = # Staged | # Main > # Staged       | # Main < # Staged
----------------------------------------------------------------
 All nodes in      | (# Main - # Staged)     | (# Staged - # Main)
 node_id_diff      | have been removed,      | have been added,
 have moved        |                         |
                   | (# Staged -             | (# Staged - len(node_intersection))
                   | len(node_intersection)) | have moved   
                   | have moved              | 
```
