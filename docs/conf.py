# -*- coding: utf-8 -*-
from __future__ import unicode_literals


extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.autosummary',
    'sphinx.ext.coverage',
    'sphinx.ext.doctest',
    'sphinx.ext.extlinks',
    'sphinx.ext.ifconfig',
    'sphinx.ext.napoleon',
    'sphinx.ext.todo',
    'sphinx.ext.viewcode',
    'recommonmark',
    'sphinx_markdown_tables',
    'nbsphinx',
]
source_suffix = '.rst'
master_doc = 'index'
project = 'treediffer'
year = '2020'
author = 'Ivan Savov'
copyright = '{0}, {1}'.format(year, author)
version = release = '0.0.1'


exclude_patterns = [
    'examples/.ipynb_checkpoints',
    'examples/drafts',
    '_build',
    'build',
]


pygments_style = 'trac'
templates_path = ['.']
extlinks = {
    'issue': ('https://github.com/learningequality/treediffer/issues/%s', '#'),
    'pr': ('https://github.com/learningequality/treediffer/pull/%s', 'PR #'),
}
html_theme = "sphinx_rtd_theme"

html_use_smartypants = True
html_last_updated_fmt = '%b %d, %Y'
html_split_index = False
html_sidebars = {
   '**': ['searchbox.html', 'globaltoc.html', 'sourcelink.html'],
}
html_short_title = '%s-%s' % (project, version)

napoleon_use_ivar = True
napoleon_use_rtype = False
napoleon_use_param = False


source_suffix = ['.md', '.rst', '.ipynb']

linkcheck_ignore = [r'http://localhost:.*?', r'https://docs.google.com/spreadsheets.*?']
