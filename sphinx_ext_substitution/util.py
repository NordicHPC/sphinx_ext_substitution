
from .get_replacements import get_substitutions

def make_sub_rst(id_, x):
    """Turn (id, original) into valid RST which can be inserted in a document for parsing."""
    return ":sub:`(%s)%s`"%(id_, x.replace("`", r"\`").strip())
