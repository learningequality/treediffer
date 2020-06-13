

# RICECOOKER TREES
################################################################################

assessment_items_key = 'questions'

ricecooker_map = {
    "license_id": "license.license_id",
    "license_description": "license.description",
    "copyright_holder": "license.copyright_holder",
}


# RICECOOKER->STUDIO TREES
################################################################################


assessment_items_key = 'questions'

ricecooker_studio_map = {
}


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



# KOLIBRI TREES
################################################################################

assessment_items_key = None

setlike_attrs = [
    "tags",
    "assessmentmetadata",  # ASSESSMENT items are actually list-like, but handle as a set for simplicity
]

kolibri_map = {
    "license_id": "license_name",
    "copyright_holder": "license_owner",
}

