import copy
import logging
import pprint

from .diffutils import contains, findby, treefindby, get_descendants
from .presets import diff_presets

logger = logging.getLogger('treediffs')
logger.setLevel(logging.DEBUG)


# EXTERNAL API
################################################################################

def treediff(treeA, treeB, preset=None, format="simplified", sort_order_changes=False,
             attrs=None, exclude_attrs=[], mapA={}, mapB={},
             assessment_items_key='assessment_items', setlike_attrs=['tags']):
    """
    Compute the diff between `treeA` (old tree) and `treeB` (new tree).
    """
    # 0. load diff preset
    if preset is not None:
        if preset in diff_presets:
            kwargs = diff_presets[preset]
            attrs = kwargs['attrs'] if 'attrs' in kwargs else attrs
            exclude_attrs = kwargs['exclude_attrs'] if 'exclude_attrs' in kwargs else exclude_attrs
            mapA = kwargs['mapA'] if 'mapA' in kwargs else mapA
            mapB = kwargs['mapB'] if 'mapB' in kwargs else mapB
            assessment_items_key = kwargs['assessment_items_key'] if 'assessment_items_key' in kwargs else assessment_items_key
            setlike_attrs = kwargs['setlike_attrs'] if 'setlike_attrs' in kwargs else setlike_attrs

            # print(preset, format, sort_order_changes, attrs, exclude_attrs, mapA, mapB, assessment_items_key, setlike_attrs)

    # 1. compute the tree diff
    # special handling of tree root nodes??? (might not have the same IDs)
    raw_diff = diff_subtree(None, treeA, None, treeB, root=True,
                            attrs=attrs, exclude_attrs=exclude_attrs,
                            mapA=mapA, mapB=mapB,
                            assessment_items_key=assessment_items_key,
                            setlike_attrs=setlike_attrs)


    # 2. detect node moves
    nodes_moved = detect_moves(raw_diff['nodes_deleted'], raw_diff['nodes_added'])
    raw_diff['nodes_moved'] = nodes_moved

    if format == "raw" and sort_order_changes:
        # keep sort_order changes and count them as moves
        return raw_diff
    elif format == "raw" and not sort_order_changes:
        # filter out nodes for which only sort_order has changed (local moves)
        new_nodes_moved = [nm for nm in nodes_moved if not nm['sort_order_change']]
        raw_diff['nodes_moved'] = new_nodes_moved
        return raw_diff

    # 3. simplify (remove nodes moved from nodes added/deleted lists)
    simplified_diff = simplify_diff(raw_diff)
    if format == "simplified" and sort_order_changes:
        return simplified_diff
    elif format == "simplified" and not sort_order_changes:
        # filter out nodes for which only sort_order has changed (local moves)
        nodes_moved = simplified_diff['nodes_moved']
        new_nodes_moved = [nm for nm in nodes_moved if not nm['sort_order_change']]
        simplified_diff['nodes_moved'] = new_nodes_moved
        return simplified_diff

    # 4. restructure (un-flatten)
    restructured_diff = restructure_diff(simplified_diff, treeA, treeB, mapA=mapA, mapB=mapB)
    if not sort_order_changes:
        # filter out nodes for which only sort_order has changed (local moves)
        nodes_moved = restructured_diff['nodes_moved']
        new_nodes_moved = [nm for nm in nodes_moved if not nm['sort_order_change']]
        restructured_diff['nodes_moved'] = new_nodes_moved
    if format == "restructured":
        return restructured_diff



# INTERNAL API
################################################################################

def diff_subtree(parent_idA, nodeA, parent_idB, nodeB, root=False,
    attrs=None, exclude_attrs=[], mapA={}, mapB={},
    assessment_items_key='assessment_items', setlike_attrs=['tags']):
    """
    Compute the changes between the node `nodeA` in the old tree and the
    corresponding `nodeB` in the new tree. This is the main workhorse call and
    includes diff of attributes, and recusive diff of node's children.
    """
    if root:
        # special handling for root node of the tree
        node_id_keyA = mapA.get('root.node_id', 'node_id')   # a.k.a. channel_id
        node_id_keyB = mapB.get('root.node_id', 'node_id')   # a.k.a. channel_id
        content_id_keyB = mapB.get('root.content_id', 'content_id')
    else:
        # regular nodes
        node_id_keyA = mapA.get('node_id', 'node_id')
        node_id_keyB = mapB.get('node_id', 'node_id')
        content_id_keyB = mapB.get('content_id', 'content_id')

    # Get IDs for nodeA and nodeB
    node_idA = nodeA[node_id_keyA]
    node_idB, content_idB = nodeB[node_id_keyB], nodeB[content_id_keyB]

    attrs_diff = diff_attributes(nodeA, nodeB, root=root,
                                 attrs=attrs, exclude_attrs=exclude_attrs,
                                 mapA=mapA, mapB=mapB,
                                 assessment_items_key=assessment_items_key,
                                 setlike_attrs=setlike_attrs)
    nodes_modified = []
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


# NODE ATTRIBUTES
################################################################################

def diff_attributes(nodeA, nodeB, root=False,
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
        attrs.update( set(mapA.keys()).union(set(mapB.keys())) )
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
            or attr == assessment_items_key or attr == 'files' or attr == 'children':
            continue

        attrA = mapA.get(attr, attr)
        attrB = mapB.get(attr, attr)

        if attrA not in nodeA and attrB not in nodeB:
            logger.warning("requested diff for missing attr " + attr)
            continue
        elif attrA not in nodeA:
            attributes[attr] = {'value': nodeB[attrB]}
            added.append(attr)
        elif attrB not in nodeB:
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

        if attrA not in nodeA and attrB not in nodeB:
            continue
        elif attrA not in nodeA:
            attributes[attr] = {'value': nodeB[attrB]}
            added.append(attr)
        elif attrB not in nodeB:
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
        files_diff = diff_files(nodeA['files'], nodeB['files'], exclude_attrs=exclude_attrs, mapA=mapA, mapB=mapA)
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
        listA = nodeA[assessment_items_key]
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


def diff_files(listA, listB, exclude_attrs=[], mapA={}, mapB={}):
    """
    Compute the diff of two lists for files, treating them as set-like.
    """
    added = []
    deleted = []

    cleanlistA = []
    for fileA in listA:
        cleanfileA = fileA.copy()
        for exclude_attr in exclude_attrs:
            if exclude_attr.startswith('files.'):
                file_attr = exclude_attr.replace('files.', '')
                cleanfileA.pop(file_attr)
        cleanlistA.append(cleanfileA)

    cleanlistB = []
    for fileB in listB:
        cleanfileB = fileB.copy()
        for exclude_attr in exclude_attrs:
            if exclude_attr.startswith('files.'):
                file_attr = exclude_attr.replace('files.', '')
                cleanfileB.pop(file_attr)
        cleanlistB.append(cleanfileB)

    for cleanfileA in cleanlistA:
        if cleanfileA not in cleanlistB:
            deleted.append(cleanfileA)
    for cleanfileB in cleanlistB:
        if cleanfileB not in cleanlistA:
            added.append(cleanfileB)
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
    # 1A. prepropocess listA to extract order and assessment_id
    itemsA = []
    assessment_idsA = set()
    for i, aiA in enumerate(listA):
        assessment_id_keyA = mapA.get('assessment_id', 'assessment_id')
        assessment_idA = aiA[assessment_id_keyA]
        order_keyA = mapA.get('order', 'order')
        orderA = aiA.get(order_keyA, None)
        if orderA is None:
            orderA = float(i + 1)  # 1-based indexitng
        itemA = dict(
            order=orderA,
            assessment_id=assessment_idA,
            assessment_item=aiA,
        )
        itemsA.append(itemA)
        assessment_idsA.add(assessment_idA)

    # 1B. prepropocess listB to extract order and assessment_id
    itemsB = []
    assessment_idsB = set()
    for j, aiB in enumerate(listB):
        assessment_id_keyB = mapB.get('assessment_id', 'assessment_id')
        assessment_idB = aiB[assessment_id_keyB]
        order_keyB = mapB.get('order', 'order')
        orderB = aiB.get(order_keyB, None)
        if orderB is None:
            orderB = float(j + 1)  # 1-based indexitng
        itemB = dict(
            order=orderB,
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

        # remove order attribute of the assessment_item
        aiA, aiB = itA['assessment_item'], itB['assessment_item']
        aiAattrs, aiBattrs = copy.deepcopy(aiA), copy.deepcopy(aiB)
        order_keyA = mapA.get('order', 'order')
        if order_keyA in aiAattrs:
            aiAattrs.pop(order_keyA)
        order_keyB = mapB.get('order', 'order')
        if order_keyB in aiBattrs:
            aiBattrs.pop(order_keyB)

        # remove attribute from the exclude_attrs dict
        for exclude_attr in exclude_attrs:
            if exclude_attr.startswith('assessment_items.'):
                ai_attr = exclude_attr.replace('assessment_items.', '')
                aiAattrs.pop(ai_attr)
                aiBattrs.pop(ai_attr)

        files_changed = False
        if 'files' in aiA and 'files' in aiB:
            aiAattrs.pop('files')
            aiBattrs.pop('files')
            files_diff = diff_files(aiA['files'], aiB['files'], exclude_attrs=exclude_attrs, mapA=mapA, mapB=mapA)
            if files_diff['added'] or files_diff['deleted']:
                files_changed = True

        if aiAattrs == aiBattrs and itA['order'] == itB['order'] and not files_changed:
            continue  # same attrs and same sort order, so not modified or moved
        elif aiAattrs == aiBattrs and not files_changed and itA['order'] != itB['order']:
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



# TREE STUCTURE
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
            sort_orderA = float(i + 1)  # 1-based indexitng
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
            sort_orderB = float(j + 1)  # 1-based indexitng
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
        flatlist = flatten_subtree(parent_idA, item['sort_order'], item['node'], kind="deleted", map=mapA)
        nodes_deleted.extend(flatlist)

    # 3. nodes added
    nodes_added = []
    added_items = [itB for itB in itemsB if not contains(itemsA, itB, by=('node_id', 'sort_order'))]
    for item in added_items:
        flatlist = flatten_subtree(parent_idB, item['sort_order'], item['node'], kind="added", map=mapB)
        nodes_added.extend(flatlist)

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
    interpret those nodes as having moved. Returns `nodes_moved` (list).
    """
    nodes_deleted_old_node_id = {}
    for node in nodes_deleted:
        nodes_deleted_old_node_id[node['old_node_id']] = node

    nodes_added_by_new_node_id = {}
    for node in nodes_added:
        nodes_added_by_new_node_id[node['node_id']] = node

    nodes_moved_by_new_node_id = {}
    for old_node_id, nd in nodes_deleted_old_node_id.items():
        for new_node_id, na in nodes_added_by_new_node_id.items():
            if nd['content_id'] == na['content_id']:
                if new_node_id not in nodes_moved_by_new_node_id.keys():
                    nm = copy.deepcopy(na)
                    nm['old_node_id'] = old_node_id
                    nm['old_parent_id'] = nd['old_parent_id']
                    nm['old_sort_order'] = nd['old_sort_order']
                    nodes_moved_by_new_node_id[new_node_id] = nm
                else:
                    logger.info('A node move with content_id=' + nd['content_id'] + ' already exists.')

    nodes_moved = []
    for nm in nodes_moved_by_new_node_id.values():
        if nm['old_parent_id'] == nm['parent_id'] and nm['old_node_id'] == nm['node_id']:
            nm['sort_order_change'] = True
        else:
            nm['sort_order_change'] = False
        nodes_moved.append(nm)

    return nodes_moved


# PHASE 3: simplify to avoid nodes moved showing up in added and deleted
################################################################################

def simplify_diff(raw_diff):
    """
    For presentation purposes, nodes that were recognized as "moved" don't need
    to show up in the `nodes_deleted` and `nodes_added` lists.
    """
    nodes_moved = raw_diff['nodes_moved']
    old_node_ids_moved = set(nm['old_node_id'] for nm in nodes_moved)
    new_node_ids_moved = set(nm['node_id'] for nm in nodes_moved)

    nodes_deleted = raw_diff['nodes_deleted']
    new_nodes_deleted = [nd for nd in nodes_deleted if nd['old_node_id'] not in old_node_ids_moved]

    nodes_added = raw_diff['nodes_added']
    new_nodes_added = [na for na in nodes_added if na['node_id'] not in new_node_ids_moved]

    simplified_diff = {
        'nodes_deleted': new_nodes_deleted,
        'nodes_added': new_nodes_added,
        'nodes_moved': nodes_moved,
        'nodes_modified': raw_diff['nodes_modified'],
    }
    return simplified_diff



# PHASE 4: restructure for displaying diffs in tree form
################################################################################

def restructure_diff(simplified_diff, treeA, treeB, mapA={}, mapB={}):
    """
    Go thorugh flatlists of nodes deleted, added, and moved and organize them
    into subtrees to make get a more compact representation for display purposes.
    """
    node_id_keyA = mapA.get('node_id', 'node_id')
    node_id_keyB = mapB.get('node_id', 'node_id')

    def restrucute_list(difflist, parent_id_key="parent_id", diff_node_id_key="node_id",
                        tree=None, by="node_id"):
        """
        Restucture list of diff nodes `difflist` by identifing complere subtrees
        of changes. The logic used is to loop over all diff nodes in `difflist`,
        get all their descendants the tree `tree` and do the restructuing if all
        the descendants are also in `difflist`.
        Returns a list of individual nodes and restructured node subtrees.
        """
        # 1. store for the restructured nodes:
        nodes_by_id = dict((node[diff_node_id_key], node) for node in difflist)
        # 2. a shallow copy of 1. to use as pointers to all nodes for lookups
        pointers_to_nodes = nodes_by_id.copy()
        all_node_ids = set(nodes_by_id.keys())
        #
        node_ids_restructured = set()
        for diff_node_id in all_node_ids:
            if diff_node_id in node_ids_restructured:
                continue  # skip nodes thave have already been restrucutred
            assert diff_node_id in nodes_by_id, 'must be still in list'
            #
            # now let's lookup node_id in the tree and get its descendants
            tree_node = treefindby(tree, diff_node_id, by=by)
            descendants = get_descendants(tree_node, include_self=False)
            descendants_ids = set(dnode[by] for dnode in descendants)
            if descendants_ids and descendants_ids.issubset(all_node_ids):
                # full subtree rooted at tree_node in list, so let's restrucutre
                for dtree_node in descendants:
                    dnode_id = dtree_node[by]
                    if dnode_id in nodes_by_id:
                        # this descendant hasn't been restructured yet, do it!
                        ddiff_node = nodes_by_id.pop(dnode_id)
                        parent_id = ddiff_node[parent_id_key]
                        parent_diff_node = pointers_to_nodes[parent_id]
                        if 'children' in parent_diff_node:
                            parent_diff_node['children'].append(ddiff_node)
                        else:
                            parent_diff_node['children'] = [ddiff_node]
                        node_ids_restructured.add(dnode_id)
                    else:
                        logger.debug('node ' + dnode_id + ' has already been restructured')
            else:
                pass  # no restructuring: leave diff_node in nodes_by_id for now
        return list(nodes_by_id.values())

    nodes_deleted = simplified_diff['nodes_deleted']
    new_nodes_deleted = restrucute_list(nodes_deleted,
        parent_id_key="old_parent_id", diff_node_id_key="old_node_id",
        tree=treeA, by=node_id_keyA)

    nodes_added = simplified_diff['nodes_added']
    new_nodes_added = restrucute_list(nodes_added,
        parent_id_key="parent_id", diff_node_id_key="node_id",
        tree=treeB, by=node_id_keyB)

    nodes_moved = simplified_diff['nodes_moved']
    new_nodes_moved = restrucute_list(nodes_moved,
        parent_id_key="parent_id", diff_node_id_key="node_id",
        tree=treeB, by=node_id_keyB)

    restructured_diff = {
        'nodes_deleted': new_nodes_deleted,
        'nodes_added': new_nodes_added,
        'nodes_moved': new_nodes_moved,
        'nodes_modified': simplified_diff['nodes_modified'],
    }
    return restructured_diff
