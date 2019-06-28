import re

from docutils import nodes
from docutils.parsers.rst import Directive

from sphinx.locale import _
from sphinx.util.docutils import SphinxDirective

import sphinx.util.nodes

class sub(nodes.Admonition, nodes.Element):
    pass

id_re = re.compile("^(?:  \(?([^():]+)  [):]   \s+?)", re.VERBOSE)

#class sub(nodes.General, nodes.Element):
#    pass

data = {
    'A2-id': 'A2-substitute',
    'A4-id': '*A4-substitute*',

    'A11-id': '''\
A11.1-substitute

*A11.2-substitute*
''',
    }


#class Data():


def get_substitutions(config):
    return data



def visit_sub_node(self, node):
    self.visit_admonition(node)

def depart_sub_node(self, node):
    self.depart_admonition(node)

def sub_role(name, rawtext, text, lineno, inliner,
             options={}, content=[]):
    """Substitute roles text"""
    mode = inliner.document.settings.env.config.substitute_mode
    subs = get_substitutions(inliner.document.settings.env.config)
    print('=====')

    # the ID and the non-ID original content
    m = id_re.match(text)
    print("text:", text)
    if m:
        print("id_=", m.group(1), m.end())
        id_ = m.group(1)
        content = text[m.end():]
        print("content=", content)
    else:
        id_ = 'NO_ID'
        content = text
        print("content=", content)

    # Find the replacement value, don't use it for anything yet.
    if id_ in subs:
        replacement = subs[id_]
    else:
        replacement = None
    print('replacement=', replacement)

    # Create new text based on mode, original, and replacement.
    if mode == 'both':
        if replacement:
            content = content + ' ' + replacement
        else:
            pass  # content stays the same, what we had before
        content, messages = inliner.parse(content, lineno, inliner, inliner)
    elif mode == 'original' or replacement is None:
        content, messages = inliner.parse(content, lineno, inliner, inliner)
    elif mode == 'replace':
        content, messages = inliner.parse(replacement, lineno, inliner, inliner)
    else:
        raise ValueError("bad value of substitute_mode")

    #import pdb ; pdb.set_trace()
    print("final content=", content)
    return content, messages


from docutils import statemachine
#from docutils.core import publish_doctree

#import sphinx.directives#import Directive
#print(dir(sphinx.directives))
#from sphinx.util.docutils import SphinxDirective
class SubDirective(SphinxDirective):
    required_arguments = 1
    has_content = True
    def run(self):
        mode = self.config.substitute_mode
        subs = get_substitutions(self.config)
        content = self.content
        #import pdb ; pdb.set_trace()

        # Find the ID, if any exists
        if len(self.arguments) >= 1:
            id_ = self.arguments[0]
        else:
            id_ = 'NO_ID'

        # Get the replacement value, don't use it yet
        if id_ in subs:
            replacement = subs[id_]
            replacement = statemachine.StringList(
                                    replacement.splitlines(), source='file')
        else:
            replacement = None

        # Create our new text ("result") based on mode, content, and
        # replacement.
        if mode == 'both':
            if replacement:
                content = content + replacement
            else:
                pass  # content stays content
            node = nodes.paragraph()
            self.state.nested_parse(content, self.content_offset, node)
            result = [node]
        elif mode == 'original' or replacement is None:
            node = nodes.paragraph()
            self.state.nested_parse(content, self.content_offset, node)
            result = [node]
        elif mode == 'replace':  # default
            if replacement is None:
                replacement = content
            node = nodes.paragraph()
            self.state.nested_parse(replacement, self.content_offset, node)
            result = [node]
        else:
            raise ValueError("bad value of substitute_mode")

        return result



def setup(app):
    app.add_directive("sub", SubDirective)
    app.add_role('sub', sub_role)

    app.add_config_value('substitute_path', ['.'], 'env')
    app.add_config_value('substitute_mode', 'replace', 'env')

    return {
        'version': '0.1',
        'parallel_read_safe': True,
        'parallel_write_safe': True,
        }
