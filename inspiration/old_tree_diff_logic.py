


from itertools import chain

from le_utils.constants import content_kinds



# Used to get diff between nodes
CONTENT_METADATA_FIELDS = ["title", "description", "license_id", "license_description", "language_id", "copyright_holder",
                    "extra_fields", "author", "aggregator", "provider", "role_visibility", "kind_id", "content_id"]
ASSESSMENT_EDIT_FIELDS = ['assessment_id', 'type', 'question', 'hints', 'answers', 'order', 'raw_data', 'source_url', 'randomize']
FILE_EDIT_FIELDS = ["checksum", "preset_id", "language_id", "source_url", "file_format_id"]




def get_full_node_diff(channel):
    """ Create dict of differences between main and staging trees
        Example: {
            "nodes_modified": [
                "<node_id (str)>": {
                    "attributes": {
                        "title": {
                            "changed": (bool),
                            "value": (str)
                        },
                        "files": ([{
                            "filename": (str),
                            "file_size": (int),
                            "preset": (str)
                        }]),
                        "assessment_items": ([AssessmentItem]),
                        "tags": ([Tag]),
                        ...
                    }
                },
                ...
            ],
            "nodes_added": [
                "<node_id (str)>": { "new_parent": (str),  "attributes": {...}},
                ...
            ],
            "nodes_deleted": [
                "<node_id (str)>": {"old_parent": (str), "attributes": {...}},
                ...
            ],
            "nodes_moved": [
                "<node_id (str)>": {"old_parent": (str), "new_parent": (str), "attributes": {...}},
                ...
            ]
        }


        Determining if node is added/moved/removed:

        Node id captures whether or not the (parent node_id, node_id) edge exists
        # Main = # of times content id is in main tree
        # Staged = # of times content id is in staging tree
        node_id_diff = union(Main node ids, Staged node ids) - intersection(Main node ids, Staged node ids)

         # Main = # Staged | # Main > # Staged       | # Main < # Staged
        ----------------------------------------------------------------
         All nodes in      | (# Main - # Staged)     | (# Staged - # Main)
         node_id_diff      | have been removed,      | have been added,
         have moved        | (# Staged -             | (# Staged -
                           | len(node_intersection)) |    len(node_intersection))
                           | have moved              | have moved
    """
    diff = {
        "nodes_added": {},
        "nodes_deleted": {},
        "nodes_modified": {},
        "nodes_moved": {}
    }

    staged_descendants = channel.staging_tree.get_descendants()
    main_descendants = channel.main_tree.get_descendants()

    # Go through all changed nodes
    changed_nodes = staged_descendants.filter(changed=True)
    for node in changed_nodes:
        # Get all changed fields
        if node.changed_staging_fields:
            diff['nodes_modified'].update({
                node.node_id: node.changed_staging_fields
            })

    # TODO: Once upgraded to Django 1.11, use difference and intersection
    # see https://docs.djangoproject.com/en/1.11/ref/models/querysets/#django.db.models.query.QuerySet.difference
    staged_content_ids = staged_descendants.values_list('content_id', flat=True)
    main_content_ids = main_descendants.values_list('content_id', flat=True)
    for content_id in list(set(chain(staged_content_ids, main_content_ids))):
        # Get nodes associated to the content id
        main_nodes = main_descendants.filter(content_id=content_id)
        main_node_ids = main_nodes.values_list('node_id', flat=True)
        staged_nodes = staged_descendants.filter(content_id=content_id).order_by('changed')

        node_intersection = staged_nodes.filter(node_id__in=main_node_ids).values_list('node_id', flat=True)
        staged_nodes_diff = staged_nodes.exclude(node_id__in=node_intersection)
        main_nodes_diff = main_nodes.exclude(node_id__in=node_intersection)

        count_difference = main_nodes.count() - staged_nodes.count()
        if count_difference > 0:
            # Nodes have been deleted on the staging tree
            for deleted in main_nodes_diff.reverse()[:count_difference]:
                diff['nodes_deleted'].update({
                    deleted.node_id: {
                        "old_parent": deleted.parent.node_id,
                        "attributes": get_node_dict(deleted),
                    }
                })

        elif count_difference < 0:
            # Nodes have been added on the staging tree
            for added in staged_nodes_diff.reverse()[:abs(count_difference)]:
                diff['nodes_added'].update({
                    added.node_id: {
                        "old_parent": added.parent.node_id,
                        "attributes": get_node_dict(added)
                    }
                })

        # Handle moved nodes
        min_index = min(main_nodes.count(), staged_nodes.count())
        for index in range(min_index - node_intersection.count()):
            main_moved_node = main_nodes_diff[index]
            staged_moved_node = staged_nodes_diff[index]

            diff['nodes_moved'].update({
                staged_moved_node.node_id: {
                    "old_parent": main_moved_node.parent.node_id,
                    "new_parent": staged_moved_node.parent.node_id,
                    "old_node_id": main_moved_node.node_id,
                    "attributes": get_node_diff(staged_moved_node, main_moved_node),
                }
            })

    return diff


def get_node_dict(node):
    data = { field: getattr(node, field) for field in CONTENT_METADATA_FIELDS }
    data.update({"files": list(node.files.values(*FILE_EDIT_FIELDS))})
    data.update({"assessment_items": list(node.assessment_items.values(*ASSESSMENT_EDIT_FIELDS))})
    data.update({"tags": list(node.tags.values_list('tag_name', flat=True))})
    return data




#  Diff functions
################################################################################

def set_node_diff(node, channel):
    """ Get a dict of changed fields between the main tree and the staging tree, setting changed field accordingly """
    descendants = channel.main_tree.get_descendants().prefetch_related('files', 'tags', 'assessment_items').select_related("parent")

    # Determine if node is new or moved
    original_node = descendants.filter(node_id=node.node_id).first() # If this returns something, node is just modified
    if not original_node:
        copies = descendants.filter(content_id=node.content_id).exists() # If there are copies, the node was moved

    if original_node:
        node.changed_staging_fields = get_node_diff(node, original_node)

        # If there are any changes, set the changed attribute and save
        if node.changed_staging_fields.items():
            node.changed = True
            node.save()

def get_node_diff(node, original_node):
    # Check for metadata field changes
    changed_fields = {
        field: getattr(node, field)
        for field in CONTENT_METADATA_FIELDS
        if getattr(node, field) != getattr(original_node, field)
    }

    # Check for file changes
    file_diff = get_file_diff2(node, original_node)
    if file_diff.items():
        changed_fields.update({"files": file_diff})

    # Check for tag changes
    tag_diff = get_tag_diff(node, original_node)
    if tag_diff.items():
        changed_fields.update({"tags": tag_diff})

    # Check for assessment_item changes
    ai_diff = get_assessment_item_diff(node, original_node)
    if ai_diff.items():
        changed_fields.update({"assessment_items": ai_diff})

    return changed_fields


def get_file_diff2(node, original_node):
    file_diff = {}

    # Get new files
    old_presets = original_node.files.values_list('preset_id', flat=True)
    new_files = node.files.exclude(preset_id__in=old_presets).values(*FILE_EDIT_FIELDS)
    if new_files:
        file_diff.update({"new": [dict(item) for item in new_files]})

    # Get modified files
    changed_files = []
    for f in node.files.filter(preset_id__in=old_presets):
        original_file = original_node.files.get(preset_id=f.preset_id)
        file_changes = {
            field: getattr(f, field)
            for field in FILE_EDIT_FIELDS
            if getattr(f, field) != getattr(original_file, field)
        }
        if file_changes.items():
            file_changes.update({"preset_id": f.preset_id})
            changed_files.append(file_changes)
    if changed_files:
        file_diff.update({"modified": changed_files})

    # Get deleted files
    new_presets = node.files.values_list('preset_id', flat=True)
    deleted_files = original_node.files.exclude(preset_id__in=new_presets).values(*FILE_EDIT_FIELDS)
    if deleted_files:
        file_diff.update({"deleted": [dict(item) for item in deleted_files]})

    return file_diff

def get_tag_diff(node, original_node):
    tag_diff = {}

    # Get added tags
    original_tag_names = original_node.tags.values_list('tag_name', flat=True)
    new_tags = node.tags.exclude(tag_name__in=original_tag_names).values_list('tag_name', flat=True)
    if new_tags:
        tag_diff.update({"new": list(new_tags)})

    # Get deleted tags
    new_tag_names = node.tags.values_list('tag_name', flat=True)
    deleted_tags = original_node.tags.exclude(tag_name__in=new_tag_names).values_list('tag_name', flat=True)
    if deleted_tags:
        tag_diff.update({"deleted": list(deleted_tags)})

    return tag_diff

def get_assessment_item_diff(node, original_node):
    ai_diff = {}

    # Only check exercises
    if node.kind_id != content_kinds.EXERCISE:
        return ai_diff

    # Get new assessment items
    old_ais = original_node.assessment_items.values_list('assessment_id', flat=True)
    new_ais = node.assessment_items.exclude(assessment_id__in=old_ais).values(*ASSESSMENT_EDIT_FIELDS)
    if new_ais:
        ai_diff.update({"new": [dict(item) for item in new_ais]})

    # Get modified assessment_items
    changed_ais = []
    for ai in node.assessment_items.filter(assessment_id__in=old_ais):
        original_ai = original_node.assessment_items.get(assessment_id=ai.assessment_id)
        ai_changes = {
            field: getattr(ai, field)
            for field in ASSESSMENT_EDIT_FIELDS
            if getattr(ai, field) != getattr(original_ai, field)
        }
        if ai_changes.items():
            ai_changes.update({"assessment_id": ai.assessment_id})
            changed_ais.append(ai_changes)
    if changed_ais:
        ai_diff.update({"modified": changed_ais})

    # Get deleted assessment_items
    new_ais = node.assessment_items.values_list('assessment_id', flat=True)
    deleted_ais = original_node.assessment_items.exclude(assessment_id__in=new_ais).values(*ASSESSMENT_EDIT_FIELDS)
    if deleted_ais:
        ai_diff.update({"deleted": [dict(item) for item in deleted_ais]})

    return ai_diff
