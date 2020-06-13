#!/usr/bin/env python
import argparse
import copy
import csv
from datetime import datetime
import dictdiffer
import json
import os
import requests

from ricecooker.config import LOGGER






# Studio Tree Local Cache queries
################################################################################


def print_channel_tree(channel_tree):
    """
    Print tree structure.
    """
    def print_tree(subtree, indent=''):
        kind = subtree.get("kind", 'topic')  # topic default to handle channel root
        if kind == "exercise":
            print(indent, subtree['title'],
                          'kind=', subtree['kind'],
                          len(subtree['assessment_items']), 'questions',
                          len(subtree['files']), 'files')
        else:
            print(indent, subtree['title'],
                          'kind=', subtree['kind'],
                          len(subtree['files']), 'files')
        for child in subtree['children']:
            print_tree(child, indent=indent+'    ')
    print_tree(channel_tree)









# CSV CORRECTIONS LOADERS
################################################################################



def unresolve_children(node):
    """
    Return copy of node with children = list of studio_id references instead of full data.
    """
    node =  copy.deepcopy(node)
    if 'children' in node:
        new_children = []
        for child in node['children']:
            new_children.append(child['id'])
        node['children'] = new_children
    return node






# SPECIAL REMAP NEEDED FOR ALDARYN CORRECTIONS
################################################################################

def remap_original_source_node_id_to_node_id(channel_tree, corrections_by_original_source_node_id):
    ALL_COORECTIONS_KINDS = ['nodes_modified', 'nodes_added', 'nodes_deleted', 'nodes_moved']
    corrections_by_node_id = {}
    for correction_kind in ALL_COORECTIONS_KINDS:
        if correction_kind in corrections_by_original_source_node_id:
            corrections_by_node_id[correction_kind] = {}
            corrections_dict = corrections_by_original_source_node_id[correction_kind]
            for original_source_node_id, correction in corrections_dict.items():
                results = find_nodes_by_original_source_node_id(channel_tree, original_source_node_id)
                assert results, 'no match found based on original_source_node_id search'
                assert len(results)==1, 'multiple matches found...'
                tree_node = results[0]
                node_id = tree_node['node_id'] 
                corrections_by_node_id[correction_kind][node_id] = correction
    return corrections_by_node_id






