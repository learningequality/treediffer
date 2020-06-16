treediffer
==========

[![build](https://travis-ci.com/learningequality/treediffer.svg?branch=master)](https://travis-ci.com/github/learningequality/treediffer)


A library of utility functions for computing diffs between tree-like data structures.

<!--
[![docs](https://readthedocs.org/projects/treediffer/badge/?style=flat)](https://readthedocs.org/projects/treediffer)
[![pypi](https://img.shields.io/pypi/pyversions/treediffer.svg)](https://pypi.python.org/pypi/treediffer/)
[![codecov](https://codecov.io/gh/learningequality/treediffer/branch/master/graphs/badge.svg?branch=master)](https://codecov.io/github/learningequality/treediffer)
[![version](https://img.shields.io/pypi/v/treediffer.svg)])https://pypi.org/project/treediffer)
[![supported-implementations](https://img.shields.io/pypi/implementation/treediffer.svg)](https://pypi.org/project/treediffer)
-->


Installation
------------

    pip install treediffer



Usage
-----
```python

from treediffer import treediff, studio_trees_options

diff = treediff(maintree, stagingtree, **studio_trees_options)

```

Documentation
-------------

https://treediffer.readthedocs.io/




TODOs
-----
 -[ ] Finish basic functionality
 -[ ] Consider adding `copied` field (a special type of added, where a node with
      the same content_id in the old tree exists)
 -[ ] Assumes `content_id` available on topic nodes (may need to relax in future)

