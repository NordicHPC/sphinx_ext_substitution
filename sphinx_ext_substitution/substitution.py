from docutils import nodes
from docutils.parsers.rst import Directive

from sphinx.locale import _
from sphinx.util.docutils import SphinxDirective

import sphinx.util.nodes

class sub(nodes.Admonition, nodes.Element):
    pass


#class sub(nodes.General, nodes.Element):
#    pass

data = {
    'id-A2': 'substitute-A2',
    'id-A4': '*substitute-A4*',
    }


def visit_sub_node(self, node):
    self.visit_admonition(node)


def depart_sub_node(self, node):
    self.depart_admonition(node)

def sub_role(name, rawtext, text, lineno, inliner,
             options={}, content=[]):
    if ':' not in text:
        return inliner.parse(text, lineno, inliner, inliner)
    id_, content = text.split(':', 1)
    if id_ in data:
        content = data[id_]
    content = content.lstrip(' ')
    #import pdb ; pdb.set_trace()
    content, messages = inliner.parse(content, lineno, inliner, inliner)
    return content, messages



class SubDirective(Directive):
    required_arguments = 1
    has_content = True
    def run(self):
        return [nodes.paragraph("Hello, world!")]


        #paragraph_node = nodes.paragraph(text='Hello World!')
        #return [paragraph_node]

def setup(app):
    app.add_directive("sub", SubDirective)
    app.add_role('sub', sub_role)

    return {
        'version': '0.1',
        'parallel_read_safe': True,
        'parallel_write_safe': True,
        }
