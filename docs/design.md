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
