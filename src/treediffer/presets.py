# DIFF PRESETS
################################################################################

diff_presets = {}   # preset -> kwargs to pass to difftree function




# RICECOOKER INTERNAL TREES
################################################################################

assessment_items_key = 'questions'

ricecooker_map = {
    "license_id": "license.license_id",
    "license_description": "license.description",
    "copyright_holder": "license.copyright_holder",
}


# RICECOOKER->STUDIO TREE (wire format)
################################################################################

ricecooker_studio_map = {}

diff_presets['ricecooker'] = dict(
    assessment_items_key='questions',
    mapA=ricecooker_studio_map.copy(),
    mapB=ricecooker_studio_map.copy(),
)



# STUDIO TREES
################################################################################

assessment_items_key = 'assessment_items'

STUDIO_NODE_ATTRIBUES = [
    "title", "description", "license_id", "license_description", "language_id", "copyright_holder",
    "extra_fields", "author", "aggregator", "provider", "role_visibility", "kind_id", "content_id"
]

STUDIO_ASSESSMENT_ITEM_ATTRIBUES = [
    'assessment_id', 'type', 'question', 'hints', 'answers', 'order', 'raw_data', 'source_url', 'randomize'
]

STUDIO_FILE_ATTRIBUES = ["checksum", "preset_id", "language_id", "source_url", "file_format_id"]

# TODO diff_presets['studio']



# KOLIBRI TREES
################################################################################

kolibri_map = {
    "node_id": "id",
    "license_id": "license_name",
    "copyright_holder": "license_owner",
}

diff_presets['kolibri'] = dict(
    assessment_items_key=None,
    setlike_attrs=[
        "tags",
        "assessment_item_ids",  # assessment items are actually list-like, but handle as a set for simplicity
    ],
    mapA=kolibri_map.copy(),
    mapB=kolibri_map.copy(),
)

