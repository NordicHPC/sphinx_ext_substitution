import os
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


class Original(nodes.strong):
    #classes = ['ss-original']
    pass

class Replacement(nodes.emphasis):
    pass

class OriginalBlock(nodes.strong):
    #classes = ['ss-original']
    pass

class ReplacementBlock(nodes.emphasis):
    pass


def visit_original(self, node):
    raise
    self.body.append('<strong>')
def depart_original(self, node):
    raise
    self.body.append('</strong>')

def visit_replacement(self, node):
    raise
    self.body.append('<em>')
def depart_replacement(self, node):
    raise
    self.body.append('</em>')

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
        original = text[m.end():]
        print("original=", original)
    else:
        id_ = 'NO_ID'
        original = text
        print("original=", original)

    # Find the replacement value, don't use it for anything yet.
    if id_ in subs:
        replacement = subs[id_]
    else:
        replacement = None
    print('replacement=', replacement)

    # Create new text based on mode, original, and replacement.
    if mode == 'both':
        #content = [ ]
        messages = [ ]
        content = nodes.Element()

        # Make original
        original1, messages1 = inliner.parse(original, lineno, inliner, inliner)
        print(original1)
        #node1 = nodes.Element()
        node1 = nodes.strong()
        node1 += nodes.Text('(%s) '%id_)
        node1 += original1
        #node1['classes'].append('ss-original')
        print(node1)
        #import pdb ; pdb.set_trace()
        node1.attributes['classes'].append('substitute-original')
        node1['styles'] = ["color: green"]
        #node1.attributes['style'] = "color: green"
        #content.append(node1)
        content += node1
        messages.append(messages1)
        print("BOTH: node1=", node1)

        # Add replacement if needed
        if replacement:
            original2, messages2 = inliner.parse(replacement, lineno, inliner, inliner)
            #node2 = Replacement()
            node2 = nodes.emphasis()
            node2 += original2
            #node2 += original2
            node2.attributes['classes'].append('substitute-replacement')
            node2['style'] = "color: blue"
            print("BOTH: node2=", node2)

            #x = nodes.Element()
            #content.append(node2)
            #content = content + node2

            x = Replacement()
            x += node2
            content = content + x
            messages.append(messages2)
        print("BOTH: content=", content)

        messages = messages[0]
        #content = content[0] + content[1]
    elif mode == 'original' or replacement is None:
        content, messages = inliner.parse(original, lineno, inliner, inliner)
        node1 = Original()
        node1 += content
        content = node1
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

def doctree(app, doctree_):
    print('DOCTREE')
    print(doctree_)
    for x in doctree_:
        print('   ', x)


def init_static_path(app):
    static_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '_static'))
    app.config.html_static_path.append(static_path)

def setup(app):
    app.add_directive("sub", SubDirective)
    app.add_role('sub', sub_role)
    app.connect('doctree-read', doctree)

    app.add_config_value('substitute_path', ['.'], 'env')
    app.add_config_value('substitute_mode', 'replace', 'env')

    app.add_node(Original,
                 html=(visit_original, depart_original),
                 html4css1=(visit_original, depart_original),
                 )
    app.add_node(Replacement,
                 html=(visit_replacement, depart_replacement),
                 html4css1=(visit_replacement, depart_replacement),
                 )

    # Hint is from https://github.com/choldgraf/sphinx-copybutton/blob/master/sphinx_copybutton/__init__.py
    app.connect('builder-inited', init_static_path)
    app.add_stylesheet("sphinx_ext_substitution.css")

    return {
        'version': '0.1',
        'parallel_read_safe': True,
        'parallel_write_safe': True,
        }
