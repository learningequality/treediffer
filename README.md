treediffer
==========

[![version](https://img.shields.io/pypi/v/treediffer.svg)](https://pypi.org/project/treediffer)
[![build](https://travis-ci.com/learningequality/treediffer.svg?branch=master)](https://travis-ci.com/github/learningequality/treediffer)
[![codecov](https://codecov.io/gh/learningequality/treediffer/branch/master/graphs/badge.svg?branch=master)](https://codecov.io/github/learningequality/treediffer)
[![pypi](https://img.shields.io/pypi/pyversions/treediffer.svg)](https://pypi.python.org/pypi/treediffer/)
[![docs](https://readthedocs.org/projects/treediffer/badge/?style=flat)](https://readthedocs.org/projects/treediffer) 


A library of utility functions for computing diffs between tree-like data structures.


Installation
------------

    pip install treediffer



Usage example
-------------
Given studio tree JSON-archive versions of the `maintree` and the `stagingtree`
of a Studio channel generated using `./contentcuration/manage.py archivechannel ...`,
you can compute the tree diff between them using:

```python
>>> from treediffer import treediff
>>> diff = treediff(maintree, stagingtree, preset="studio", format="simplified")
>>> diff
{
  "nodes_deleted": [...],   # content_ids gone in stagingtree
  "nodes_added": [...],     # new content_ids in stagingtree
  "nodes_moved": [...],     # same content_id but different node_id
  "nodes_modified": [...],  # same node_id, but changes in node attributes
}
```
This code examples uses the "high level" API based on the studio preset that set
all the necessary lookups (node_id, content_id, parent, assetment_items, etc.)
so the diffing logic will work. See ` examples/studiodiffferpoc.py` for full script.


### Ricecooker tree diffing
See `examples/ricecookerdiffpoc.py` for similar script that diffs ricecooker trees
that get saved in `chefdata/trees/` dir after each content integration script runs.



Alternative diff formats
------------------------
Use `format="restructured"` to post-process the simplified diff and group additions
and deletions into logical subtrees (e.g. if whole topic is deleted, show as subtree).
This is the default when printing on command line as in the example scripts.

Use `format="raw"` to see the diff before simplification and move detection (for debugging).



Tests
-----

    pytest

and 

    pytest --cov=src/treediffer tests/





Documentation
-------------
Visit https://treediffer.readthedocs.io/ for more info about how this works
In particular see https://treediffer.readthedocs.io/en/latest/diff_formats.html
for the the details about the structure of the diffs produced and 
https://treediffer.readthedocs.io/en/latest/design.html for API advanced usage.




TODOs
-----

 - [x] Finish basic functionality
 - [x] add example ricecooker differ
 - [x] add example studio differ
 - [ ] Add kitchen sink test for combined deleted, added, moved, and modified

