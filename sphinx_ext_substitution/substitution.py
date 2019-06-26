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
    'A2-id': 'A2-substitute',
    'A4-id': '*A4-substitute*',

    'A11-id': '''\
A11.1-substitute

*A11.2-substitute*
''',
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


from docutils import statemachine
#from docutils.core import publish_doctree

class SubDirective(Directive):
    required_arguments = 1
    has_content = True
    def run(self):
        content = self.content
        #print(content)
        #print(type(content), type(content[1]))
        id_ = self.arguments[0]

        if id_ in data:
            content = data[id_]
            #print(content)
            #content = nodes.paragraph(content)
            #content =  content.split('\n')
            #content = statemachine.string2lines(content, 4,
            #                                          convert_whitespace=True)
            #content = publish_doctree(content)

            content = statemachine.StringList(
                                    content.splitlines(), source='file')


            #print('===')
            #print(content)
            #print(type(content), type(content[1]))

        node = nodes.paragraph()
        self.state.nested_parse(content, self.content_offset, node)

        return [node]




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
