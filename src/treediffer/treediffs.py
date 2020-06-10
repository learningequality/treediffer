import pprint

from .diffutils import list2dict, contains

def compare_node_attrs(nodeA, nodeB, attrs):
    diff = []
    for attr in attrs:
        attrA = nodeA.get(attr, None)
        attrB = nodeA.get(attr, None)
        if attrA != attrB:
            diff.append(attr)
    return diff


def diff_lists(listA, listB, parent_idA, parent_idB, attrs=['title'], mapA={}, mapB={}, recursive=True):
    """
    Compute the diff between the nodes in `listA` and the noddes in `listB`.
    Args:
      - attrs (list(str)): what attributes to check in comparison
      - mapA: map of diff attribues in listA node attributes
      - mapB: map of diff attribues to listB node attributes
      - recursive (bool): check just one level of children, or all levels of children?
    """
    # 1A. prepropocess listA nodes
    itemsA = []
    node_idsA = set()
    content_idsA = set()
    for i, nodeA in enumerate(listA):
        node_id_keyA = mapA.get('node_id', 'node_id')
        content_id_keyA = mapA.get('content_id', 'content_id')
        node_idA, content_idA = nodeA[node_id_keyA], nodeA[content_id_keyA]
        sort_order_keyA = mapA.get('sort_order', 'sort_order')
        sort_orderA = nodeA.get(sort_order_keyA, None)
        if sort_orderA is None:
            sort_orderA = i + 1  # 1-based indexitng
        itemA = dict(
            parent_id=parent_idA,
            node_id=node_idA,
            sort_order=sort_orderA,
            content_id=content_idA,
            node=nodeA,
        )
        itemsA.append(itemA)
        node_idsA.add(node_idA)
        content_idsA.add(content_idA)

    # 1B. prepropocess listB nodes
    itemsB = []
    node_idsB = set()
    content_idsB = set()
    for j, nodeB in enumerate(listB):
        node_id_keyB = mapB.get('node_id', 'node_id')
        content_id_keyB = mapB.get('content_id', 'content_id')
        node_idB, content_idB = nodeB[node_id_keyB], nodeB[content_id_keyB]
        sort_order_keyB = mapB.get('sort_order', 'sort_order')
        sort_orderB = nodeB.get(sort_order_keyB, None)
        if sort_orderB is None:
            sort_orderB = j + 1  # 1-based indexitng
        itemB = dict(
            parent_id=parent_idB,
            node_id=node_idB,
            sort_order=sort_orderB,
            content_id=content_idB,
            node=nodeB,
        )
        itemsB.append(itemB)
        node_idsB.add(node_idB)
        content_idsB.add(content_idB)

    # 2. compare lists
    deleted_items = [itA for itA in itemsA if not contains(itemsB, itA, by=('node_id','sort_order'))]
    added_items = [itB for itB in itemsB if not contains(itemsA, itB, by=('node_id','sort_order'))]

    # 3. check modifications

    # 4. recurse

    # format nodes_deleted for diff output
    nodes_deleted = []
    for item in deleted_items:
        node = dict(
            old_node_id=item['node_id'],
            old_parent_id=item['parent_id'],
            old_sort_order=item['sort_order'],
            content_id=item['content_id'],
            attributes=dict(
                (attr, {'value': val}) for attr, val in item['node'].items()
            )
        )
        nodes_deleted.append(node)

    # format nodes_added for diff output
    nodes_added = []
    for item in added_items:
        node = dict(
            node_id=item['node_id'],
            parent_id=item['parent_id'],
            sort_order=item['sort_order'],
            content_id=item['content_id'],
            attributes=dict(
                (attr, {'value': val}) for attr, val in item['node'].items()
            )
        )
        nodes_added.append(node)


    diff = dict(
        nodes_deleted=nodes_deleted,
        nodes_added=nodes_added,
    )

    # for node_pair in node_pairs:
    #     childA, childB = children_pair
    #     children_attr_diff = compare_node_attrs(childA, childB, attrs=attrs, mapA=mapA, mapB=mapB)
    #     diff.extend(children_attr_diff)
    #     if recursive:
    #         children_diff = compare_trees_children(childA, childB, attrs=attrs, mapA=mapA, mapB=mapB, recursive=recursive)
    #         diff.extend(children_diff)
    return diff



def compare_trees_children(nodeA, nodeB, attrs=['title'], mapA={}, mapB={}, recursive=True):
    """
    Check children of nodeA and nodeB are identical.
    Args:
      - attrs (list(str)): what attributes to check in comparison
      - mapA: map of attribues in attr to nodeA attributes
      - mapB: map of attribues in attr to nodeB attributes
      - recursive (bool): compare just the two lists or also compare dec
    """
    diff = []
    childrenA = nodeA.get('children', [])
    childrenB = nodeB.get('children', [])
    if not childrenA and not childrenB:
        return []
    if childrenA and not childrenB or not childrenA and childrenB:
        return ['different children']
    elif childrenA and childrenB:
        children_pairs = zip(childrenA, childrenB)
        for children_pair in children_pairs:
            childA, childB = children_pair
            children_attr_diff = compare_node_attrs(childA, childB, attrs=attrs, mapA=mapA, mapB=mapB)
            diff.extend(children_attr_diff)
            if recursive:
                children_diff = compare_trees_children(childA, childB, attrs=attrs, mapA=mapA, mapB=mapB, recursive=recursive)
                diff.extend(children_diff)
    return diff


def compare_subtrees(nodeA, nodeB, attrs=['title'], mapA={}, mapB={}):
    """
    Recucsively compare subtrees at `nodeA` and `nodeB`.
    Returns empty list if no difference found.
    """
    diff = []
    # 1. Check attributes are identical
    attrs_diff = compare_node_attrs(nodeA, nodeB, attrs=attrs, mapA=mapA, mapB=mapB)
    diff.extend(attrs_diff)
    # 2. Check children are identical
    children_diff = compare_trees_children(nodeA, nodeB, attrs=attrs, mapA=mapA, mapB=mapB)
    diff.extend(children_diff)
    return diff





def treediff(oldtree, newtree, ignoreattrs=None, treekeys=['children', 'questions', 'files']):
    """
    Compute the differences between `newtree` and `oldtree`.
    """
    diff_dict = {
        "nodes_deleted": {},
        "nodes_added": {},
        "nodes_moved": {},
        "nodes_modified": {},
    }




