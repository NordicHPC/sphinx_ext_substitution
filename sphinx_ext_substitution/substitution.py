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


#class Data():


def get_substitutions(config):
    return data



def visit_sub_node(self, node):
    self.visit_admonition(node)

def depart_sub_node(self, node):
    self.depart_admonition(node)

def sub_role(name, rawtext, text, lineno, inliner,
             options={}, content=[]):

    print(dir(inliner))
    inliner.document.settings.config #.substitute_path #config #settings.env.app.config
    mode = inliner.document.settings.env.config.substitute_mode
    subs = get_substitutions(inliner.document.settings.env.config)

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

#import sphinx.directives#import Directive
#print(dir(sphinx.directives))
#from sphinx.util.docutils import SphinxDirective
class SubDirective(SphinxDirective):
    required_arguments = 1
    has_content = True
    def run(self):
        content = self.content
        id_ = self.arguments[0]

        mode = self.config.substitute_mode
        subs = get_substitutions(self.config)

        import pdb ; pdb.set_trace()

        if id_ in data:
            content = data[id_]
            content = statemachine.StringList(
                                    content.splitlines(), source='file')

        node = nodes.paragraph()
        self.state.nested_parse(content, self.content_offset, node)

        return [node]




        #paragraph_node = nodes.paragraph(text='Hello World!')
        #return [paragraph_node]

#if not app.config.todo_include_todos

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
