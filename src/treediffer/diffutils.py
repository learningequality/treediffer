import copy
import functools
import os
import pprint


# LIST/SET UTILS
################################################################################

def list2dict(alist, by="node_id"):
    """
    Convert a list of nodes to a dict whose keys taken from the item's `by` attr.
    """
    adict = {}
    for item in alist:
        key = item[by]
        adict[key] = item
    return adict


def findallby(container, item, by="node_id"):
    """
    Find all occurences of item in container (list or dict) based on key `by`.
    Return a list of occurences or an empty list if not found.
    """
    results = []
    if isinstance(container, dict):
        container = container.values()
    if type(by) == str:
        for el in container:
            if el[by] == item[by]:
                results.append(el)
    elif type(by) == tuple:
        keys = by
        for el in container:
            if all(el[key] == item[key] for key in keys):
                results.append(el)
    else:
        raise ValueError('Match keys `by` support only strings or tupes.')
    return results


def findby(container, item, by="node_id"):
    """
    Look for item in the container (list or dict) based on the key in `by`.
    Return first occurence of the item if found or None if not found.
    """
    results = findallby(container, item, by=by)
    if results:
        return results[0]
    else:
        return None


def contains(container, item, by="node_id"):
    """
    Check if item appears in container (list or dict) based on the key in `by`.
    """
    match = findby(container, item, by=by)
    if match:
        return True
    else:
        return False


def rget(dict_obj, attrpath):
    """
    A fancy version of `get` that allows getting dot-separated nested attributes
    like `license.license_name` for use in tree comparisons attribute mappings.
    This code is inspired by solution in https://stackoverflow.com/a/31174427.
    """
    def _getnoerrors(dict_obj, attr):
        """
        Like regular get but will no raise if `dict_obj` is None.
        """
        if dict_obj is None:
            return None
        return dict_obj.get(attr)
    return functools.reduce(_getnoerrors, [dict_obj] + attrpath.split('.'))



# TREE UTILS
################################################################################

def treefindby(subtree, value, by="node_id"):
    """
    Returns node in `subtree` that has attribute `by` equal to `value`.
    """
    results = treefindallby(subtree, value, by=by)
    if len(results) == 1:
        return results[0]
    elif len(results) > 1:
        print("WARNING: multiple results found matching " + by + "=" + value)
        return results[0]
    else:
        print("WARNING: no results found matching " + by + "=" + value)
        return None


def treefindallby(subtree, value, by="node_id"):
    """
    Returns all node in `subtree` that have attribute `by` equal to `value`.
    """
    results = []
    if by in subtree and subtree[by] == value:
        results.append(subtree)
    if 'children' in subtree:
        for child in subtree['children']:
            child_results = treefindallby(child, value, by=by)
            results.extend(child_results)
    return results


def get_descendants(node, include_self=True):
    """
    Return a flat list including `node` and all its descendants. Nodes returned
    are modified to remove the tree structure between them (set `children=[]`).
    """
    results = []
    if include_self:
        node_copy = copy.deepcopy(node)
        node_copy['children'] = []
        results.append(node_copy)
    if 'children' in node:
        for child in node['children']:
            child_results = get_descendants(child, include_self=True)
            results.extend(child_results)
    return results


# DIFF PRINTING
################################################################################

DEFAULT_ATTRS = ['title']
DEFAULT_IDS = ['node_id', 'parent_id']

def get_attr_diff_str(diffkind, attribute):
    if diffkind == 'deleted':
        return colormap['deleted'](attribute['value'])
    elif diffkind == 'added':
        return colormap['added'](attribute['value'])
    elif diffkind == 'moved':
        return colormap['moved'](attribute['value'])
    elif diffkind == 'modified':
        if 'old_value' in attribute and attribute['old_value'] != attribute['value']:
            return colormap['deleted'](attribute['old_value']) + '->' + colormap['added'](attribute['value'])
        else:
            return attribute['value']

def get_id_diff_str(diffkind, node, id_key):
    old_id_key = 'old_' + id_key
    if diffkind == 'deleted':
        if old_id_key in node:
            return colormap['deleted'](node[old_id_key])
    elif diffkind == 'added':
        if id_key in node:
            return colormap['added'](node[id_key])
    elif diffkind == 'moved':
        if node[old_id_key] != node[id_key]:
            return colormap['deleted'](node[old_id_key]) + '->' + colormap['added'](node[id_key])
        else:
            return node[id_key]
    elif diffkind == 'modified':
        return node[id_key]


def print_diff_node(diffkind, node, indent=0, attrs=DEFAULT_ATTRS, ids=DEFAULT_IDS):
    line = colormap[diffkind]('  '*indent + '- ')
    
    # attrs
    attr_strs = []
    for attr in attrs:
        attributes = node['attributes']
        attr_str = get_attr_diff_str(diffkind, attributes[attr])
        attr_strs.append(attr_str)
    line += ', '.join(attr_strs) + ' '

    # ids
    id_strs = []
    for id in ids:
        id_str = id + ':' + str(get_id_diff_str(diffkind, node, id))
        id_strs.append(id_str)
    line += '(' + ', '.join(id_strs) + ')'

    print(line)

    # all modified attrs
    if diffkind == 'modified':
        for attr, attr_vals in node['attributes'].items():
            if attr in attrs or attr in ids:
                pass # continue
            elif 'old_value' in attr_vals and bool(attr_vals['old_value']) == False and bool(attr_vals['value']) == False:
                continue
            elif 'old_value' in attr_vals:
                attrline = '  '*indent + '    > ' + attr + ': '
                old_val = attr_vals['old_value'] or ''
                new_val = attr_vals['value'] or ''
                if len(old_val) > 100 and len(new_val) > 100:
                    attrline += colormap['deleted'](old_val[0:50] + '...')
                    attrline += '->' + colormap['added'](new_val[0:50] + '...')
                else:
                    attrline += colormap['deleted'](old_val)
                    attrline += '->' + colormap['added'](new_val)
                print(attrline)

    if 'children' in node:
        for child in node['children']:
            print_diff_node(diffkind, child, indent=indent+1, attrs=attrs, ids=ids)


def print_difflist(diffkind, difflist, attrs=DEFAULT_ATTRS, ids=DEFAULT_IDS):
    assert diffkind in colormap.keys(), 'unknown diffkind ' + diffkind
    print('\n' + colormap[diffkind]("Nodes " + diffkind + ':'))
    for node in difflist:
        print_diff_node(diffkind, node, indent=0, attrs=attrs, ids=ids)


def print_diff(diff, attrs=DEFAULT_ATTRS, ids=DEFAULT_IDS):
    """
    Print the diff to the terminal using color coding. The node attributes in
    `attrs` will be displayed (e.g. title) as well `ids` (node_id and parent_id).
    """
    for key, difflist in diff.items(): 
        if difflist:
            diffkind = key.replace('nodes_', '')
            print_difflist(diffkind, difflist, attrs=attrs, ids=ids)




# TERMINAL COLORS
################################################################################

def _wrap_with(code):
    """
    Wrap text with ANSI color codes for terminal printing.
    via https://github.com/ploxiln/fab-classic/blob/master/fabric/colors.py
    """
    def inner(text, bold=False):
        c = code
        if os.environ.get('DISABLE_COLORS'):
            return text
        if bold:
            c = "1;%s" % c
        return "\033[%sm%s\033[0m" % (c, text)
    return inner

red = _wrap_with('31')
green = _wrap_with('32')
yellow = _wrap_with('33')
blue = _wrap_with('34')
magenta = _wrap_with('35')
cyan = _wrap_with('36')

colormap = {
    'deleted': red,
    'added': green,
    'moved': blue,
    'modified': magenta,
}

