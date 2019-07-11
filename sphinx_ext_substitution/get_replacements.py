from __future__ import print_function

import os
from os.path import join as pjoin
import glob

try:
    import yaml
except ImportError:
    yaml = None

testdata = {
    'A2-id': 'A2-substitute',
    'A4-id': '*A4-substitute*',

    'A11-id': '''\
A11.1-substitute

*A11.2-substitute*
''',
    }

# Global state of substitutions.  This is *only* used in this module,
# and currently used *only* as a global cache: once loaded, do not
# reload.
SUBSTITUTIONS = { }

def _load_yaml(fname, substitutions):
    if yaml is None:
        raise RuntimeError("The yaml module is needed (python-yaml) to get definitions from yaml files.")
    data = yaml.load(open(fname), Loader=yaml.SafeLoader)
    for key, value in data.items():
        if key not in substitutions:
            substitutions[key] = value.strip()

def load_substitutions(config):
    """Load substitutions from disk.  Cache results to SUBSTITUTIONS.

    Usually you will use get_substitutions, which is smarter about
    caching and config.
    """
    substitutions = SUBSTITUTIONS
    paths = config.substitute_path
    # Split by ':', even if Sphinx puts the string variable into a
    # list.
    if len(paths) == 1 and ':' in paths[0]:
        paths = paths[0].split(':')
    elif isinstance(paths, str):
        paths = paths.split(':')
    if os.environ.get('SPHINX_EXT_SUBSTITUTION_PATH', ''):
        paths[0:0] = os.environ['SPHINX_EXT_SUBSTITUTION_PATH'].split(':')
    for path in paths:
        # Directly load YAML files given in the path.
        if os.path.isfile(path):
            _load_yaml(path, SUBSTITUTIONS)
            continue
        # Load ID.rst files
        for fname in glob.glob(pjoin(path, '*.rst')):
            id_ = os.path.basename(fname)[:-4]
            if id_ not in substitutions:
                substitutions[id_] = open(fname).read().strip()
        # Load *.yaml files
        for fname in glob.glob(pjoin(path, '*.yaml')):
            _load_yaml(fname, SUBSTITUTIONS)

    return substitutions



def get_substitutions(config):
    """Get substitutions.  This is the main entrypoint to get all substitutions."""
    if SUBSTITUTIONS:
        return SUBSTITUTIONS
    if config.substitute_path == ['TESTDATA']:
        return testdata
    return load_substitutions(config)
