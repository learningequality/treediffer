# RICECOOKER->STUDIO TREES
################################################################################




# STUDIO TREES
################################################################################

STUDIO_NODE_ATTRIBUES = [
    "title", "description", "license_id", "license_description", "language_id", "copyright_holder",
    "extra_fields", "author", "aggregator", "provider", "role_visibility", "kind_id", "content_id"
]

STUDIO_ASSESSMENT_ITEM_ATTRIBUES = [
    'assessment_id', 'type', 'question', 'hints', 'answers', 'order', 'raw_data', 'source_url', 'randomize'
]

STUDIO_FILE_ATTRIBUES = ["checksum", "preset_id", "language_id", "source_url", "file_format_id"]






# UTILS
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
    if attr in attr_map:
        attr = attr_map[attr]
    if isinstance(node, cc.ContentNode):
        return rgetattr(node, attr)
    else:
        return node[attr]
