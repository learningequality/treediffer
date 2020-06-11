import pprint

from .diffutils import contains

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
      - mapA: map of diff attribues to listA node attributes
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


def diff_node(nodeA, nodeB,
    attrs=None, exclude_attrs=[], mapA={}, mapB={},
    listlike_attrs=['assesment_items'],
    setlike_attrs=['tags', 'files'],
):
    # Get nodeA info
    node_id_keyA = mapA.get('node_id', 'node_id')
    content_id_keyA = mapA.get('content_id', 'content_id')
    node_idA, content_idA = nodeA[node_id_keyA], nodeA[content_id_keyA]
    sort_order_keyA = mapA.get('sort_order', 'sort_order')
    sort_orderA = nodeA.get(sort_order_keyA, None)

    # Get nodeB info
    node_id_keyB = mapB.get('node_id', 'node_id')
    content_id_keyB = mapB.get('content_id', 'content_id')
    node_idB, content_idB = nodeB[node_id_keyB], nodeB[content_id_keyB]
    sort_order_keyB = mapB.get('sort_order', 'sort_order')
    sort_orderB = nodeB.get(sort_order_keyB, None)



def diff_attributes(nodeA, nodeB,
    attrs=None, exclude_attrs=[], mapA={}, mapB={},
    listlike_attrs=['assesment_items'],
    setlike_attrs=['tags', 'files'],
):
    """
    Compute the diff between the attrributes of `nodeA` and `nodeB`.
    Returns a dict { added=[], deleted=[], modifeid=[], attributes={} }
    """
    attributes = {}
    added, deleted, modified = [], [], []

    if attrs is None:
        # Calculate "all attrs" based on the node attrs and the given attr-maps
        attrs = set()
        attrs.update( set(mapA.keys()).union(set(mapA.keys())) )
        #
        mapA_vals = set(mapA.values())
        mapB_vals = set(mapB.values())        
        for keyA in nodeA.keys():
            if keyA not in mapA_vals:
                attrs.add(keyA)
        for keyB in nodeB.keys():
            if keyB not in mapB_vals:
                attrs.add(keyB)
        attrs = sorted(attrs) 

    # 1. Regular attributes
    for attr in attrs:
        if attr in exclude_attrs or attr in listlike_attrs or attr in setlike_attrs:
            continue

        attrA = mapA.get(attr, attr)
        attrB = mapB.get(attr, attr)

        if nodeA.get(attrA) is None and nodeB.get(attrB) is None:
            print("WARNING requested diff for attr " + attr + "that don't exist")
            continue
        elif nodeA.get(attrA) is None:
            attributes[attr] = {'value': nodeB[attrB]}
            added.append(attr)
        elif nodeB.get(attrB) is None:
            attributes[attr] = {'old_value': nodeA[attrA]}
            deleted.append(attr)
        elif nodeA[attrA] == nodeB[attrB]:
            # no difference
            attributes[attr] = {'value': nodeB[attrB]}
        else:
            # both exist and there is a difference
            attributes[attr] = {'old_value': nodeA[attrA], 'value': nodeB[attrB]}
            modified.append(attr)

    # 2. Set-like attributes
    for attr in setlike_attrs:
        attrA = mapA.get(attr, attr)
        attrB = mapB.get(attr, attr)

        if nodeA.get(attrA) is None and nodeB.get(attrB) is None:
            print("WARNING requested diff for attr " + attr + "that don't exist")
            continue
        elif nodeA.get(attrA) is None:
            attributes[attr] = {'value': nodeB[attrB]}
            added.append(attr)
        elif nodeB.get(attrB) is None:
            attributes[attr] = {'old_value': nodeA[attrA]}
            deleted.append(attr)
        else:
            # both attributes exist
            valueA_set = set(nodeA.get(attrA, []))
            valueB_set = set(nodeB.get(attrB, []))
            if valueA_set == valueB_set:
                attributes[attr] = {'value': nodeB[attrB]}
            else:
                attributes[attr] = {
                    'old_value': nodeA[attrA],
                    'value': nodeB[attrB],
                    'added': sorted(valueB_set - valueA_set),
                    'deleted': sorted(valueA_set - valueB_set),
                }
                modified.append(attr)

    # 3. List-like attributes



    return {
        'added': added,
        'deleted': deleted,
        'modified': modified,
        'attributes': attributes,
    }



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





def treediff(oldtree, newtree, attrs=None, exclude_attrs=[], mapA={}, mapB={},
             listlike_attrs=['questions'],  setlike_attrs=['tags', 'files']):
    """
    Compute the differences between `newtree` and `oldtree`.
    """
    diff_dict = {
        "nodes_deleted": {},
        "nodes_added": {},
        "nodes_moved": {},
        "nodes_modified": {},
    }




