# DIFF PRESETS
################################################################################

diff_presets = {}   # preset -> kwargs to pass to difftree function



# RICECOOKER TREE  (this is the ricecooker-->studio wire format)
################################################################################

ricecooker_map = {
    # channel attrs
    "root.node_id": "id",             # a.k.a. channel_id
    "root.content_id": "source_id",   # unique identifier within source_domain
    #
    # node attrs
    "license_name": "license.license_id",
    "license_description": "license.description",
    "copyright_holder": "license.copyright_holder",
    "role_visibility": "role",
}

diff_presets['ricecooker'] = dict(
    exclude_attrs=[
        'license',              # nested dict object; used flat attrs instead
    ],
    assessment_items_key='questions',
    mapA=ricecooker_map.copy(),
    mapB=ricecooker_map.copy(),
)



# STUDIO TREES
################################################################################

studio_exclude_attrs = [
    'id',                   # auto-generated uuid key (studio internal id)
    'tree_id',              # main and staging trees have different `tree_id`s
    'parent_id',            # auto-generated uuid key (studio internal id)
    'lft',                  # MPTT annotations (no need to track)
    'rght',                 # MPTT annotations (no need to track)
    'thumbnail_encoding',   # data
    'cloned_source_id'      # deprecated
    'original_node_id',     # deprecated
    'changed',
    'modified',
    #
    # files
    'files.id',             # auto-generated uuid key
    'files.contentnode',    # points to studio internal id
    #
    # assessment_items
    'assessment_items.id',              # auto-incdementing numeric id
    'assessment_items.contentnode',     # points to studio internal id
]

studio_map = {
    "license_name": "license.license_name",
}

diff_presets['studio'] = dict(
    # assessment_items_key = 'assessment_items', # this is the default so no need
    exclude_attrs=studio_exclude_attrs,
    mapA=studio_map.copy(),
    mapB=studio_map.copy(),
)



# KOLIBRI TREES
################################################################################

kolibri_map = {
    # root node attrs
    "root.node_id": "id",
    "root.content_id": "content_id",
    #
    # regular node attrs
    "node_id": "id",
    "copyright_holder": "license_owner",
    #
    # no assessment_items attrs, since treated as set of assessment_ids
}


diff_presets['kolibri'] = dict(
    exclude_attrs=[
        'id',           # auto-generated uuid key
        'tree_id',      # main and staging trees will have different `tree_id`s
        'parent_id',    # we already handle `parent_id` as part of diff logic
        'lft',          # MPTT annotations (no need to track)
        'rght',         # MPTT annotations (no need to track)
        'level',        # tree depth (Kolibri-only)
    ],
    assessment_items_key=None,
    setlike_attrs=[
        "tags",
        "assessment_item_ids",  # assessment items are actually list-like, but handle as a set for simplicity
    ],
    mapA=kolibri_map.copy(),
    mapB=kolibri_map.copy(),
)
