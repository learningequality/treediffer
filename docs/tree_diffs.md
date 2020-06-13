Tree diffs
==========

The functions in `treediffer` are used to find differences between two trees.


### Example of node deleted
A node deletion appears under the key `nodes_deleted.{node_id}` and contains the
structural info where the deletion occurred, and the attributes of the node that was deleted:

```python
nodes_deleted = [
    {
        "old_node_id": (str),
        "old_parent_id": (str),
        "old_sort_order": (float),
        "content_id": (content_id),
        "attributes": {
            "title": {"value": "The title of the deleted node"},
            "description": {"value": "The description of the node that was deleted"},
            "content_id": {"value": (str)},
            "sort_order": {"value": (float)},
            ... }
    },
    {},
    ...,
    {},
]
```

To apply this deletion patch, find content node
`c = ContenNode.filter(tree_id=...).get(node_id=deleted['node_id'])`, and its parent
`parent_node = ContenNode.filter(tree_id=...).get(node_id=deleted['old_parent_id'])`,
then call `parent_node.children.remove(c)`. The `attributes` dict is provided
for information purposes only (e.g. to display info about the node being deleted in the UI).


### Example of node added
A node added to the tree is appears under the key `nodes_added.{node_id}` and is
represented by the following dict:

```python
nodes_added = [
    {
        "parent_id": (node_id),
        "node_id": (node_id),
        "sort_order": (float),
        "content_id": (content_id),
        "attributes": {
            "title": {"value": "The title of the new node"},
            "description": {"value": "The description of the new node"},
            "content_id": {"value": (str)},
            "sort_order": {"value": (float)},
            ... }
    },
    {},
    ...,
    {},
]
```

To apply this "patch," create a new `c = ContentNode(**map(..., attributes))`,
find the parent node where the new node is to be added,
`parent_node = ContenNode.filter(tree_id=...).get(node_id=added['parent_id'])`,
then call `parent_node.children.add(c)`.

Note: when applying a patch with multiple node additions, watch out for sort order
in systems that don't know how to handle `sort_order` (ricecooker).



### Example of node moved
Nodes in the `newtree` that have the same `content_id` as a node in the `oldtree`
but whose `node_id` has changed can be interpreted as moves. If multiple nodes
satisfy this criterion, the only the first node is treated as a move (in tree-order)
while others "node clones" of the same `content_id` are recorded as additions.


```python
nodes_moved = [
    {
        "content_id": (content_id),
        "node_id": (node_id),
        "old_node_id": (node_id),
        "parent_id": (node_id),
        "old_parent_id": (node_id),
        "sort_order": (float),
        "old_sort_order": (float),
        "attributes": {
            "title": {"value": "The title of the new node"},
            "description": {"value": "The description of the new node"},
            "content_id": {"value": (str)},
            "sort_order": {"value": (float), "old_value": (== old_sort_order)},
            ...},
    },
    {},
    ...,
    {},
]
```


### Example of node modified

When a node appears in both the "before tree" and the "after tree" in the same
`node_id` (position within the tree) but who have different attributes.
These "attribute diffs" are stored under the keys `old_value`, `value` = new value,
with special handling for set-like attributes (files and tags), and list-like
attributes (assessment_items).

Example data structure:

```python
nodes_modified = [
    {
        "node_id": (node_id),
        "parent_id": (node_id),
        "content_id": (content_id),
        # intentionally not tracking changes in sort_order since those are defined as moves
        "changed": ["title", "sort_order", "tags", "assessment_items"],
        "attributes": {
            "title":{
                "old_value": "Old title",
                "value": "The new title for the node"
            },
            "description": {"value": "The description of the new node"},
            "content_id": {"value": (str)},
            "sort_order": {"value": (float), "old_value": (== old_sort_order)},
            "tags": {                                                           # set-like
                "old_value": ['oldtag1', 'oldtag2'],
                "value": ['oldtag1', 'newtag3', 'newtag4'],
                "tags_removed": ['oldtag2'],
                "tags_added": ['newtag3', 'newtag4'],
            },
            "assessment_items": {                                               # list-like
                "old_value": [
                    {"id": "aiid1", "assessment_id": 'q1', ... },
                    {"id": "aiid2", "assessment_id": 'q2', ... },
                    {"id": "aiid3", "assessment_id": 'q3', ... }
                ],
                "value": [
                    {"id": "aiid1", "assessment_id": 'q1', ... },
                    {"id": "aiid4", "assessment_id": 'q4', ... },
                    {"id": "aiid3", "assessment_id": 'q3', ... },
                ],
                "deleted": [
                    {"id": "aiid2", "assessment_id": 'q2', ... },
                ]
                "added": [
                    {"id": "aiid4", "assessment_id": 'q4', ... },
                ]
                "moved": [],
                "modified": [],
            },
    },
    {},
    ...,
    {},
]
```



## Node structural annotations


|                	| `old_parent_id` 	| `parent_id` 	| `old_sort_order` 	| `sort_order` 	|
|-------------------|:-----------------:|:-------------:|:-----------------:|:-------------:|
| `nodes_deleted`  	| x             	|           	| x              	|            	|
| `nodes_added`   	|               	| x         	|                	| x          	|
| `nodes_moved`   	| x             	| x         	| x              	| x          	|
| `nodes_modified` 	|               	|           	|                	|            	|

