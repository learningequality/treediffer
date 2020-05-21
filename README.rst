========
Overview
========

.. start-badges

.. list-table::
    :stub-columns: 1

    * - docs
      - |docs|
    * - tests
      - | |travis|
        | |codecov|
    * - package
      - | |version| |wheel| |supported-versions| |supported-implementations|
        | |commits-since|
.. |docs| image:: https://readthedocs.org/projects/treediffer/badge/?style=flat
    :target: https://readthedocs.org/projects/treediffer
    :alt: Documentation Status

.. |travis| image:: https://api.travis-ci.org/learningequality/treediffer.svg?branch=master
    :alt: Travis-CI Build Status
    :target: https://travis-ci.org/learningequality/treediffer

.. |codecov| image:: https://codecov.io/gh/learningequality/treediffer/branch/master/graphs/badge.svg?branch=master
    :alt: Coverage Status
    :target: https://codecov.io/github/learningequality/treediffer

.. |version| image:: https://img.shields.io/pypi/v/treediffer.svg
    :alt: PyPI Package latest release
    :target: https://pypi.org/project/treediffer

.. |wheel| image:: https://img.shields.io/pypi/wheel/treediffer.svg
    :alt: PyPI Wheel
    :target: https://pypi.org/project/treediffer

.. |supported-versions| image:: https://img.shields.io/pypi/pyversions/treediffer.svg
    :alt: Supported versions
    :target: https://pypi.org/project/treediffer

.. |supported-implementations| image:: https://img.shields.io/pypi/implementation/treediffer.svg
    :alt: Supported implementations
    :target: https://pypi.org/project/treediffer

.. |commits-since| image:: https://img.shields.io/github/commits-since/learningequality/treediffer/v0.0.1.svg
    :alt: Commits since latest release
    :target: https://github.com/learningequality/treediffer/compare/v0.0.1...master



.. end-badges

A library of utility functions for coputing diffs between tree-like data structures.

* Free software: MIT license

Installation
============

::

    pip install treediffer

You can also install the in-development version with::

    pip install https://github.com/learningequality/treediffer/archive/master.zip


Documentation
=============


https://treediffer.readthedocs.io/


Development
===========

Setup virtual env::

    virtualenv -p python3.6 venv
    source venv/bin/activate
    pip install -r requirements.txt


To run the all tests run::

    tox

Note, to combine the coverage data from all the tox environments run:

.. list-table::
    :widths: 10 90
    :stub-columns: 1

    - - Windows
      - ::

            set PYTEST_ADDOPTS=--cov-append
            tox

    - - Other
      - ::

            PYTEST_ADDOPTS=--cov-append tox
