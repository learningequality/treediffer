Design
======

Given any two tree-like data structures, let's call them `oldtree` and `newtree`,
that consist of dict-like nodes with `node_id`-like and `content_id`-like attributes.

## Tree diff format
A tree diff is a dictionary that describes four types of edits:
  - `nodes_deleted`: list of nodes that were present (by `node_id`) in `oldtree` and absent in the `newtree` (by `node_id`)
  - `nodes_added`: list of nodes added to the tree (includes both nodes ADD and COPY actions)
  - `nodes_moved`: nodes in the `newtree` that have the same `content_id` as a node
    in the `oldtree` by a new `node_id` has changed. If multiple nodes satisfy
    this criterion, the only the first node is retuned (in tree-order).
  - `nodes_modified`: to be included in this list, a node in the `newtree` must
    have the same `content_id` as a node in the `oldtree` and modified attributes.


Note a node may appear in more than one of the above lists. For example a node
that was moved from location X in the tree to location Y in the tree, and whose
title was edited will appear in all four lists:
 - in the `nodes_added` list because it now appears in location Y
 - in the `nodes_deleted` list because it was removed from location X
 - in the `nodes_moved` list since we can detect the node has the same `content_id`
 - in the `nodes_modified` list because of the title edit

For more info, see the detailed diff examples in [Tree diffs](tree_diffs.html).



## Technical notes

**Invariant**: the information in a tree diff `treediff(oldtree, newtree)`, when
applied as a "patch" to the `oldtree` should produce the `newtree`.

**Data format**: each of the "diff items" in the four lists includes additional
structural annotations like  `parent_id` and all node attributes like title,
description, files, assessment items, tags, etc., even if they haven't changed
to allow for easy display of diffs and post-processing tasks.


## Diff limitations

  - Will not recognize assessment items that are moved between exercises
  - Nodes from the `oldtree` can be duplicated in several places in the `newtree`.
    The first of these uses will be recognized as a move, while all others will
    be recognized as if the nodes were added. A more appropriate way to do this
    would be to recognize them as `nodes_copied` (a special type of added, where
    a node with the same content_id in the `oldtree` exists).
  - The logic modified and moved logic assumes `content_id` is available for all
    nodes (topic nodes and content nodes). Need to watch out to make sure this
    assumption is valid in all cases where we want to use this (ricecooker, studio
    and Koilbri, and if necessary relax this in future).



## External API (High Level)

The API for this library is to call the `treediff` function which has signature:

```python
treediff(oldtree, newtree, preset=None, format="simplified",               # HL
         attrs=None, exclude_attrs=[], mapA={}, mapB={},                   # LL API
         assessment_items_key='assessment_items', setlike_attrs=['tags'])  # LL API
```

The line tagged with `HL` is the "high level" API for the library, where users
just need to specify the two trees they need diffed (e.g. `ricecooker`, `studio`,
or `kolibri`), which will set the appropriate values for the low-level API kwargs.

The `raw` format returns the diff in the "internal representation" described above
that includes duplication (primarily used for debugging), the `simplified` format
(default) removed moved nodes from the added and deleted lists but keeps all results
as flat lists. The `restructured` format tries to return the diff as "chunks" of
tree (i.e. indicate an addition of topic + 3 children as one addition, instead
of four separate additions).



## Internal API (Low Level)

The functions the `treediff` module are named `diff_` and accept the following
standard set of keyword arguments, which we'll call the "low level" API:

```python
LL = dict(
    attrs=None, exclude_attrs=[], mapA={}, mapB={},                    # LL API
    assessment_items_key='assessment_items', setlike_attrs=['tags'])   # LL API
)
```

  - `attrs` (list(str)): if specified, only these attributes will be check for differences
    the default value is set to `None` which means all values will be checked.
  - `exclude_attrs` (list(str)): do not check these attributes, e.g. for cases
     where we expect them to be different and we want to avoid false positives.
  - `mapA` (dict): map from the common diff attributes to attributes nodes in `treeA`.
  - `mapB` (dict): map from the common diff attributes to attributes nodes in `treeB`.
  - `assessment_items_key` (str): specify where to look for assessment items, in
    Studio and Kolibri leave the default value. In ricecooker, set to `questions`.
  - `setlike_attrs` (list(str)): treat these attributes as sets (i.e. order doesn't matter)

Note: in general users should not need to set the low level API params and can
instead rely on one of the presets, which will set the appropriate keyword args,
e.g. using `preset="studio"` is equivalent to call with `**studio_preset_kwargs`.


### List of functions that use the low level API

If we call the keyword args of the low level API `**LL` we can write the entire
functions of the `treediffer` library as follows:

```python
# PHASE 1: diffing
def diff_subtree(parent_idA, nodeA, parent_idB, nodeB, **LL):
    "Compute the changes between the node `nodeA` in the old tree and the..."

    def diff_attributes(nodeA, nodeB, **LL):
        "Compute the diff between the attributes of `nodeA` and `nodeB`.
        def diff_files(listA, listB):
             "Compute the diff of two lists for files, treating them as set-like.""
        def diff_assessment_items(listA, listB, **LL):
            "Compute the diff between the lists of assessment items `listA` and `listB`,

    def diff_children(parent_idA, childrenA, parent_idB, childrenB, **LL):
        "Compute the diff between the nodes in `childrenA` and the nodes in `childrenB`."

# PHASE 2: move detection
def detect_moves(nodes_deleted, nodes_added):
    "Look for nodes with the same `content_id` that appear in both lists, ..."

# PHASE 3: simplification
def simplify_diff(raw_diff):

# PHASE 4: restructuring
def restructure_diff(simplified_diff):
```

The "main" work happens in `diff_subtree` which computes the diff of node attributes
and recursively calls diff_subtree on all children down the tree (PHASE 1).
Node moves are detected are detected as a post-processing step (PHASE 2),
and so are the format conversions for presentation needs (PHASE 3 and PHASE 4).
