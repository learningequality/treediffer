import pprint
import copy

from .diffutils import contains, findby

# EXTERNAL API
################################################################################

def treediff(treeA, treeB, preset=None, format="simplified",
             attrs=None, exclude_attrs=[], mapA={}, mapB={},
             assessment_items_key='assessment_items', setlike_attrs=['tags']):
    """
    Compute the diff between `treeA` (old tree) and `treeB` (new tree).
    """
    # 0. load diff preset
    if preset is not None:
        pass

    # 1. compute the tree diff
    # special handling of tree root nodes??? (might not have the same IDs)
    raw_diff = diff_subtree(None, treeA, None, treeB,
                            attrs=attrs, exclude_attrs=exclude_attrs,
                            mapA=mapA, mapB=mapB,
                            assessment_items_key=assessment_items_key,
                            setlike_attrs=setlike_attrs)

    # 2. detect node moves
    nodes_moved = detect_moves(raw_diff['nodes_deleted'], raw_diff['nodes_added'])
    raw_diff['nodes_moved'] = nodes_moved

    if format == "raw":
        return raw_diff

    # # 3. simplify (remove nodes moved from nodes added/deleted lists)
    # simplified_diff = simplify_diff(raw_diff)
    # 
    # # 4. restructure (un-flatten)
    # simplified_diff = restructure_diff(simplified_diff)



# PHASE 1
################################################################################

def diff_subtree(parent_idA, nodeA, parent_idB, nodeB,
    attrs=None, exclude_attrs=[], mapA={}, mapB={},
    assessment_items_key='assessment_items', setlike_attrs=['tags']):
    """
    Compute the changes between the node `nodeA` in the old tree and the
    corresponding `nodeB` in the new tree. This is the main workhorse call and
    includes diff of attributes, and recusive diff of node's children.
    """
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

    nodes_modified = []
    attrs_diff = diff_attributes(nodeA, nodeB,
                                 attrs=attrs, exclude_attrs=exclude_attrs,
                                 mapA=mapA, mapB=mapB,
                                 assessment_items_key=assessment_items_key,
                                 setlike_attrs=setlike_attrs)
    if attrs_diff['added'] or attrs_diff['deleted'] or attrs_diff['modified']:
        node = dict(
            node_id=node_idB,
            parent_id=parent_idB,
            content_id=content_idB,
            attributes=attrs_diff['attributes'],
        )
        nodes_modified.append(node)

    nodes_deleted, nodes_added = [], []
    if 'children' in nodeA and 'children' in nodeB:
        children_diff = diff_children(node_idA, nodeA['children'],
                                      node_idB, nodeB['children'],
                                      attrs=attrs, exclude_attrs=exclude_attrs,
                                      mapA=mapA, mapB=mapB,
                                      assessment_items_key=assessment_items_key,
                                      setlike_attrs=setlike_attrs)
        nodes_added.extend(children_diff['nodes_added'])
        nodes_deleted.extend(children_diff['nodes_deleted'])
        nodes_modified.extend(children_diff['nodes_modified'])

    return {
        'nodes_deleted': nodes_deleted,
        'nodes_added': nodes_added,
        'nodes_modified': nodes_modified,
    }



def diff_attributes(nodeA, nodeB,
    attrs=None, exclude_attrs=[], mapA={}, mapB={},
    assessment_items_key='assessment_items', setlike_attrs=['tags']):
    """
    Compute the diff between the attributes of `nodeA` and `nodeB`.
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
        if attr in exclude_attrs or attr in setlike_attrs \
            or attr == assessment_items_key or attr == 'files':
            continue

        attrA = mapA.get(attr, attr)
        attrB = mapB.get(attr, attr)

        if nodeA.get(attrA) is None and nodeB.get(attrB) is None:
            print("WARNING requested diff for attr " + attr + " that don't exist")
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

    # 3. Files
    if 'files' not in exclude_attrs and 'files' in nodeA and 'files' in nodeB:
        files_diff = diff_files(nodeA['files'], nodeB['files'])
        if files_diff['added'] or files_diff['deleted']:
            modified.append('files')
            attributes['files'] = {
                'old_value': nodeA['files'],
                'value': nodeB['files'],
                'added': files_diff['added'],
                'deleted': files_diff['deleted'],
            }
        else:
            attributes['files'] = {
                'value': nodeB['files'],
            }

    # 4. assessment items
    if assessment_items_key and assessment_items_key in nodeA and assessment_items_key in nodeB:
        node_id_keyA = mapA.get('node_id', 'node_id')
        node_idA = nodeA[node_id_keyA]
        listA = nodeA[assessment_items_key]
        node_id_keyB = mapB.get('node_id', 'node_id')
        node_idB = nodeB[node_id_keyB]
        listB = nodeB[assessment_items_key]
        ais_diff = diff_assessment_items(listA, listB, mapA=mapA, mapB=mapB, exclude_attrs=exclude_attrs)
        if ais_diff['added'] or ais_diff['deleted'] or ais_diff['moved'] or ais_diff['modified']:
            modified.append(assessment_items_key)
            attributes[assessment_items_key] = {
                'old_value': nodeA[assessment_items_key],
                'value': nodeB[assessment_items_key],
                'added': ais_diff['added'],
                'deleted': ais_diff['deleted'],
                'moved': ais_diff['moved'],
                'modified': ais_diff['modified'],
            }
        else:
            attributes[assessment_items_key] = {
                'value': nodeB[assessment_items_key],
            }

    # return attrs_diff
    return {
        'added': added,
        'deleted': deleted,
        'modified': modified,
        'attributes': attributes,
    }


def diff_files(listA, listB):
    """
    Compute the diff of two lists for files, treating them as set-like.
    """
    added = []
    deleted = []
    for fileA in listA:
        if fileA not in listB:
            deleted.append(fileA)
    for fileB in listB:
        if fileB not in listA:
            added.append(fileB)
    return {
        'added': added,
        'deleted': deleted,
    }


def diff_assessment_items(listA, listB, exclude_attrs=[], mapA={}, mapB={}):
    """
    Compute the diff between the lists of assessment items `listA` and `listB`,
    using the key `assessment_id` to detect modifications and reorderings.
    Note: the code assumes there are no duplicate `assessment_id`s in a list.
    """
    # 1A. prepropocess listA to extract sort_order and assessment_id
    itemsA = []
    assessment_idsA = set()
    for i, aiA in enumerate(listA):
        assessment_id_keyA = mapA.get('assessment_id', 'assessment_id')
        assessment_idA = aiA[assessment_id_keyA]
        sort_order_keyA = mapA.get('sort_order', 'sort_order')
        sort_orderA = aiA.get(sort_order_keyA, None)
        if sort_orderA is None:
            sort_orderA = i + 1  # 1-based indexitng
        itemA = dict(
            sort_order=sort_orderA,
            assessment_id=assessment_idA,
            assessment_item=aiA,
        )
        itemsA.append(itemA)
        assessment_idsA.add(assessment_idA)

    # 1B. prepropocess listB to extract sort_order and assessment_id
    itemsB = []
    assessment_idsB = set()
    for i, aiB in enumerate(listB):
        assessment_id_keyB = mapB.get('assessment_id', 'assessment_id')
        assessment_idB = aiB[assessment_id_keyB]
        sort_order_keyB = mapB.get('sort_order', 'sort_order')
        sort_orderB = aiB.get(sort_order_keyB, None)
        if sort_orderB is None:
            sort_orderB = i + 1  # 1-based indexitng
        itemB = dict(
            sort_order=sort_orderB,
            assessment_id=assessment_idB,
            assessment_item=aiB,
        )
        itemsB.append(itemB)
        assessment_idsB.add(assessment_idB)

    # 2. compare lists
    added_items = [itB for itB in itemsB if not contains(itemsA, itB, by=('assessment_id'))]
    deleted_items = [itA for itA in itemsA if not contains(itemsB, itA, by=('assessment_id'))]

    # 3. check for moves and modifications in common items
    common_item_tuples = []
    for itA in itemsA:
        itB = findby(itemsB, itA, by=('assessment_id'))
        if itB:
            common_item_tuples.append((itA, itB))
    moved, modified = [], []
    for itA, itB in common_item_tuples:
        # obtain the non-sort_order subset of the assessment_item's attrubutes
        aiA, aiB = itA['assessment_item'], itB['assessment_item']
        aiAattrs, aiBattrs = copy.deepcopy(aiA), copy.deepcopy(aiB)
        sort_order_keyA = mapA.get('sort_order', 'sort_order')
        if sort_order_keyA in aiAattrs:
            aiAattrs.pop(sort_order_keyA)
        sort_order_keyB = mapB.get('sort_order', 'sort_order')
        if sort_order_keyB in aiBattrs:
            aiBattrs.pop(sort_order_keyB)

        if 'files' in aiA and 'files' in aiB:
            aiAattrs.pop('files')
            aiBattrs.pop('files')
            files_diff = diff_files(aiA['files'], aiB['files'])
            if files_diff['added'] or files_diff['deleted']:
                files_changed = True
            else:
                files_changed = False

        if aiAattrs == aiBattrs and itA['sort_order'] == itB['sort_order'] and not files_changed:
            continue  # same attrs and same sort order, so not modified or moved
        elif aiAattrs == aiBattrs and not files_changed and itA['sort_order'] != itB['sort_order']:
            moved.append(aiB)
        else:
            modified.append(aiB)

    # format for diff output
    added = [item['assessment_item'] for item in added_items]
    deleted = [item['assessment_item'] for item in deleted_items]

    return {
        'added': added,
        'deleted': deleted,
        'moved': moved,
        'modified': modified,
    }



def diff_children(parent_idA, childrenA, parent_idB, childrenB,
    attrs=None, exclude_attrs=[], mapA={}, mapB={},
    assessment_items_key='assessment_items', setlike_attrs=['tags']):
    """
    Compute the diff between the nodes in `childrenA` and the nodes in `childrenB`.
    Args:
      - attrs (list(str)): what attributes to check in comparison
      - mapA: map of diff attribues to childrenA node attributes
      - mapB: map of diff attribues to childrenB node attributes
    """
    # 1A. prepropocess childrenA nodes
    itemsA = []
    node_idsA = set()
    for i, nodeA in enumerate(childrenA):
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

    # 1B. prepropocess childrenB nodes
    itemsB = []
    node_idsB = set()
    for j, nodeB in enumerate(childrenB):
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

    # 2. nodes deleted
    nodes_deleted = []
    deleted_items = [itA for itA in itemsA if not contains(itemsB, itA, by=('node_id', 'sort_order'))]
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

    # 3. nodes added
    nodes_added = []
    added_items = [itB for itB in itemsB if not contains(itemsA, itB, by=('node_id', 'sort_order'))]
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

    # 4. recursely diff common nodes
    nodes_modified = []
    common_item_tuples = []
    for itA in itemsA:
        itB = findby(itemsB, itA, by=('node_id'))
        if itB:
            common_item_tuples.append((itA, itB))
    for itA, itB in common_item_tuples:
        diff = diff_subtree(parent_idA, itA['node'], parent_idB, itB['node'],
                            attrs=attrs, exclude_attrs=exclude_attrs,
                            mapA=mapA, mapB=mapB,
                            assessment_items_key=assessment_items_key,
                            setlike_attrs=setlike_attrs)
        nodes_deleted.extend(diff['nodes_deleted'])
        nodes_added.extend(diff['nodes_added'])
        nodes_modified.extend(diff['nodes_modified'])

    # return combined info (note: node moves will be detected at a later stage)
    return {
        'nodes_deleted': nodes_deleted,
        'nodes_added': nodes_added,
        'nodes_modified': nodes_modified,
    }


# PHASE 2
################################################################################

def detect_moves(nodes_deleted, nodes_added):
    """
    Look for nodes with the same `content_id` that appear in both lists, and
    interpret those nodes as having moved.
    Returns `nodes_moved` (list).
    """
    # flatten lists (in case added nodes have children)
    #
    return []


# PHASE 3
################################################################################


# PHASE 4
################################################################################

