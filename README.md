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



Usage
-----
```python

from treediffer import treediff

diff = treediff(maintree, stagingtree, preset="studio")

```

Documentation
-------------

https://treediffer.readthedocs.io/




TODOs
-----
 -[ ] Finish basic functionality
 -[ ] Add kitchen sink test for combined deleted, added, moved, and modified
 
