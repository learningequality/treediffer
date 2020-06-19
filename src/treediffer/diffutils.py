import copy
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



# FLATTENING
################################################################################

def flatten_subtree(parent_id, sort_order, subtree, kind, map={}):
    """
    Recusively flatten the `subtree` of nodes and return the info a a flat list.
    The diff format depends on what `kind` of diff it is: `added` or `deleted`.
    """
    subtree =  copy.deepcopy(subtree)  # to avoid modifying original tree
    flatlist = []
    node_id_key = map.get('node_id', 'node_id')
    content_id_key = map.get('content_id', 'content_id')
    sort_order_key = map.get('sort_order', 'sort_order')

    if 'children' in subtree:
        children = subtree.pop('children')
    else:
        children = []

    # first add yourself...
    if kind == "deleted":
        node = dict(
            old_node_id=subtree[node_id_key],
            old_parent_id=parent_id,
            old_sort_order=sort_order,
            content_id=subtree[content_id_key],
            attributes=dict(
                (attr, {'value': val}) for attr, val in subtree.items()
            )
        )
        flatlist.append(node)
    elif kind == "added":
        node = dict(
            node_id=subtree[node_id_key],
            parent_id=parent_id,
            sort_order=sort_order,
            content_id=subtree[content_id_key],
            attributes=dict(
                (attr, {'value': val}) for attr, val in subtree.items()
            )
        )
        flatlist.append(node)
    else:
        raise ValueError('Unexpected flatlist kind ' + str(kind) + ' found.')

    # ... then add your children
    for i, child in enumerate(children):
        sort_order = child.get(sort_order_key, None)
        if sort_order is None:
            sort_order = float(i + 1)  # 1-based indexitng
        childflatlist = flatten_subtree(subtree[node_id_key], sort_order, child, kind=kind, map=map)
        flatlist.extend(childflatlist)

    return flatlist



# ATTRIBUTE UTILS
################################################################################

def _get_children_list(node):
    if isinstance(node, cc.ContentNode):
        return list(node.children.all())
    else:
        return node.get('children', [])


def rgetattr(obj, attr, *args):
    """
    A fancy version of `getattr` that allows getting dot-separated nested attributes
    like `license.license_name` for use in tree comparisons attribute mappings.
    via https://stackoverflow.com/a/31174427
    """
    def _getattr(obj, attr):
        return getattr(obj, attr, *args)
    return functools.reduce(_getattr, [obj] + attr.split('.'))


def _get_node_attr(node, attr, attr_map={}):
    """
    To allow diff logic to work for trees of object hierarchies or json trees.
    NOT CURRENTLY USED
    """
    if attr in attr_map:
        attr = attr_map[attr]
    if isinstance(node, cc.ContentNode):
        return rgetattr(node, attr)
    else:
        return node[attr]
