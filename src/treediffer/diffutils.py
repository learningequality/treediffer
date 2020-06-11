

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


def contains(container, item, by="node_id"):
    """
    Check if item appears in container (list or dict) based on the key in `by`.
    Return first occurence of the item if found or None if not-found.
    """
    if isinstance(container, dict):
        container = container.values()
    if type(by) == str:
        for el in container:
            if el[by] == item[by]:
                return el
        return None
    elif type(by) == tuple:
        keys = by
        for el in container:
            if all(el[key] == item[key] for key in keys):
                return el
        return None
    else:
        raise ValueError('Match keys `by` support only strings or tupes.')




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
