#!/usr/bin/env python
"""
Install treediff lib in local env:

    pip install requests git+https://github.com/learningequality/treediffer

then run 

    ./studiodiffpoc.py

to generate the detailed tree diff JSON and and print the diff in terminal.
"""

import argparse
from contextlib import redirect_stdout
import copy
import io
import json
import os
import subprocess
from treediffer import treediff
from treediffer.diffutils import print_diff
import pprint
import requests


OLD_TREE_FILENAME = "studio-small-oldtree.json"
NEW_TREE_FILENAME = "studio-small-newtree.json"
REMOTE_DOWNLOAD_DIR = "https://minireference.com/static/tmp/"
LOCAL_DOWNLOAD_DIR = "downloads"

if not os.path.exists(LOCAL_DOWNLOAD_DIR):
    os.mkdir(LOCAL_DOWNLOAD_DIR)


def ensure_filename_exists(filename):
    local_path = os.path.join(LOCAL_DOWNLOAD_DIR, filename)
    if not os.path.exists(local_path):
        remote_path = os.path.join(REMOTE_DOWNLOAD_DIR, filename)
        response = requests.get(remote_path)
        with open(local_path, 'wb') as local_file:
            local_file.write(response.content)
    assert os.path.exists(local_path)
    return local_path

def get_trees():
    pathA = ensure_filename_exists(OLD_TREE_FILENAME)
    treeA = json.load(open(pathA))
    pathB = ensure_filename_exists(NEW_TREE_FILENAME)
    treeB = json.load(open(pathB))
    return treeA, treeB


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Studio tree differ')
    args = parser.parse_args()

    treeA, treeB = get_trees()
    print('loaded old tree with ', len(treeA), 'topics in root')
    print('loaded new tree with ', len(treeB), 'topics in root')

    # simplified diff = flat list; no attmpt is made to "summarize" changes
    diff = treediff(treeA, treeB, preset="studio", format="simplified")
    diff_filename = 'studio_small_tree_simplified_diff.json'
    with open(diff_filename, 'w') as jsonf:
         json.dump(diff, jsonf, indent=2, ensure_ascii=False)

    # restructured diff = show additions/deletions of subtrees as hierarchies
    diff = treediff(treeA, treeB, preset="studio", format="restructured")
    diff_filename2 = 'studio_small_tree_restructured_diff.json'
    with open(diff_filename2, 'w') as jsonf:
         json.dump(diff, jsonf, indent=2, ensure_ascii=False)

    nodes_deleted = diff['nodes_deleted']
    nodes_added = diff['nodes_added']
    nodes_moved = diff['nodes_moved']
    nodes_modified = diff['nodes_modified']

    # print('\n\nnodesdeleted:', len(nodes_deleted))  # WRONG -- need to count descendats
    # pprint.pprint(nodes_deleted[0])

    print('\n\nnodes_added:', len(nodes_added))
    # # pprint.pprint(nodes_added[0])

    print('\n\nnodes_moved:', len(nodes_moved))
    # pprint.pprint(nodes_moved[0])

    print('\n\nnodes_modified:', len(nodes_modified))
    # pprint.pprint(nodes_modified[100:120], width=200)


    print_diff(diff,
        attrs=['title', 'kind_id'],
        ids=['node_id', 'parent_id']
    )
