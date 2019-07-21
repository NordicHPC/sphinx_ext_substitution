from __future__ import print_function

import os
import re

from docutils import nodes
from docutils import statemachine
from docutils.parsers.rst import Directive

from sphinx.locale import _
import sphinx.util.nodes

from .get_replacements import get_substitutions

class sub(nodes.Admonition, nodes.Element):
    pass

id_re = re.compile(r"^(?:  \(?([^():]+)  [):]   \s*)", re.VERBOSE)

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


#def visit_original(self, node):
#    raise
#    self.body.append('<strong>')
#def depart_original(self, node):
#    raise
#    self.body.append('</strong>')
#
#def visit_replacement(self, node):
#    raise
#    self.body.append('<em>')
#def depart_replacement(self, node):
#    raise
#    self.body.append('</em>')



def sub_role(name, rawtext, text, lineno, inliner,
             options={}, content=[]):
    """Substitute roles text"""
    mode = inliner.document.settings.env.config.substitute_mode
    subs = get_substitutions(inliner.document.settings.env.config)

    # the ID and the non-ID original content
    m = id_re.match(text)
    if m:
        id_ = m.group(1)
        original = text[m.end():]
    else:
        id_ = 'NO_ID'
        original = text
    if original:
        original = original.replace('\x00`', '`')

    # Find the replacement value, don't use it for anything yet.
    if id_ in subs:
        replacement = subs[id_]
    else:
        replacement = None
    if replacement:
        replacement = replacement.replace('\x00`', '`')

    # Save list of substitutions for the sub-list directive
    env = inliner.document.settings.env
    if not hasattr(env, 'substitute_all_subs'):
        env.substitute_all_subs = { }
    if id_ != 'NO_ID':
        env.substitute_all_subs[id_] = dict(original=original,
                                            replacement=replacement,
                                            docname=env.docname)

    # Create new text based on mode, original, and replacement.
    if mode == 'both':
        #content = [ ]
        messages = [ ]
        content = nodes.Element()

        # Make original
        original1, messages = inliner.parse(original, lineno, inliner, inliner)
        node1 = nodes.strong()
        node1 += nodes.Text('(%s) '%id_)
        node1 += original1
        node1.attributes['classes'].append('substitute-original')
        #node1['styles'] = ["color: green"]
        content += node1
        # Add replacement if needed
        if replacement:
            original2, messages2 = inliner.parse(replacement, lineno, inliner, inliner)
            #node2 = Replacement()
            node2 = nodes.emphasis()
            node2 += original2
            node2.attributes['classes'].append('substitute-replacement')
            #node2['style'] = "color: blue"
            x = Replacement()
            x += node2
            content = content + x
            #messages.append(messages2)
            messages += messages2
    elif mode == 'original' or replacement is None:
        content, messages = inliner.parse(original, lineno, inliner, inliner)
        node1 = Original()
        node1 += content
        content = node1
    elif mode == 'replace':
        content, messages = inliner.parse(replacement, lineno, inliner, inliner)
    else:
        raise ValueError("bad value of substitute_mode")

    return content, messages



class SubDirective(Directive):
    required_arguments = 1
    has_content = True
    def run(self):
        env = self.state.document.settings.env
        config = env.config
        mode = config.substitute_mode
        subs = get_substitutions(config)
        original = self.content

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

        # Save list of substitutions for the sub-list directive
        def stringify(s):
            if isinstance(s, (list, statemachine.StringList)):
                return '\n'.join(s)
            return s
        if not hasattr(env, 'substitute_all_subs'):
            env.substitute_all_subs = { }
        if id_ != 'NO_ID':
            env.substitute_all_subs[id_] = dict(original=stringify(original),
                                                replacement=stringify(replacement),
                                                docname=env.docname)

        # Create our new text ("result") based on mode, content, and
        # replacement.
        if mode == 'both':
            result = []
            content = nodes.admonition()
            content['classes'].append('substitute-original')
            title_text = "%s (original)"%id_
            content += nodes.title(title_text, '', nodes.Text(title_text))
            node = nodes.paragraph()
            self.state.nested_parse(original, self.content_offset, node)
            content += node
            result.append(content)
            if replacement:
                content = nodes.admonition()
                content['classes'].append('substitute-replacement')
                title_text = "(replacement)"
                content += nodes.title(title_text, '', nodes.Text(title_text))
                node = nodes.paragraph()
                self.state.nested_parse(replacement, self.content_offset, node)
                content += node
                result[-1].append(content)
        elif mode == 'original' or replacement is None:
            node = nodes.paragraph()
            self.state.nested_parse(original, self.content_offset, node)
            result = [node]
        elif mode == 'replace':  # default
            if replacement is None:
                replacement = original
            node = nodes.paragraph()
            self.state.nested_parse(replacement, self.content_offset, node)
            result = [node]
        else:
            raise ValueError("bad value of substitute_mode")

        return result



# The sublist node is only needed because we have to insert a
# placeholder during the first pass, and come back later once we know
# all the substitutions and insert them where sub-list was requested.
class sublist(nodes.General, nodes.Element):
        pass

class SubListDirective(Directive):
    def run(self):
        # This is filled when the process_sublist event is run.
        return [sublist('')]

def purge_sublist(app, env, docname):
    """Clear out cached data when each document (file) is parsed.

    TODO: make this not a linear search?
    """
    if not hasattr(env, 'substitute_all_subs'):
        return
    all_subs = env.substitute_all_subs
    for id_ in list(all_subs.keys()):
        if all_subs[id_]['docname'] == docname:
            del all_subs[id_]

def process_sublist(app, doctree, fromdocname):
    """Find all sub-list directives and fill it with all substitutions."""
    env = app.builder.env
    if not hasattr(env, 'substitute_all_subs'):
        env.substitute_all_subs = { }
    for node in doctree.traverse(sublist):
        table = nodes.table()
        tgroup = nodes.tgroup(cols=3)
        table += tgroup

        # This is apparently required, the default is to divide 100
        # evenly by number of columns.
        col_widths = [33, 33, 33]
        for col_width in col_widths:
            colspec = nodes.colspec(colwidth=col_width)
            tgroup += colspec

        # Construct header row
        thead = nodes.thead()
        header = ["ID", "Original", "Replacement"]
        row_node = nodes.row()
        for cell in header:
            entry = nodes.entry()
            #entry += nodes.Text(cell)
            entry += nodes.paragraph(text=cell)
            row_node += entry
        thead.extend([row_node])
        tgroup += thead

        # Construct all rows
        rows = [ ]
        #for id_, (original, replacement) in sorted(USED_SUBSTITUTIONS.items()):
        for id_, data in sorted(env.substitute_all_subs.items()):
            original = data['original']
            replacement = data['replacement']
            row = [id_, original, replacement]
            row_node = nodes.row()
            for cell in row:
                entry = nodes.entry()
                if cell:
                    #entry += nodes.Text(cell)
                    entry += nodes.paragraph(text=cell)
                row_node += entry
            rows.append(row_node)
        tbody = nodes.tbody()
        tbody.extend(rows)
        tgroup += tbody

        node.replace_self([table])



# Add our custom CSS to the headers.
def init_static_path(app):
    static_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '_static'))
    app.config.html_static_path.append(static_path)



def setup(app):
    # Config values
    app.add_config_value('substitute_path', ['.'], 'env')
    app.add_config_value('substitute_mode', 'replace', 'env')

    # Roles and directives
    app.add_directive("sub", SubDirective)
    app.add_role('sub', sub_role)
    # Nodes (visitor functions do not currently work and are not needed?)
    app.add_node(Original,
                 #html=(visit_original, depart_original),
                 #html4css1=(visit_original, depart_original),
                 )
    app.add_node(Replacement,
                 #html=(visit_replacement, depart_replacement),
                 #html4css1=(visit_replacement, depart_replacement),
                 )

    # sub-list directive
    app.add_directive("sub-list", SubListDirective)
    app.connect('doctree-resolved', process_sublist)
    app.connect('env-purge-doc', purge_sublist)

    # Add CSS to build
    # Hint is from https://github.com/choldgraf/sphinx-copybutton/blob/master/sphinx_copybutton/__init__.py
    app.connect('builder-inited', init_static_path)
    app.add_stylesheet("sphinx_ext_substitution.css")

    return {
        'version': '0.1',
        'parallel_read_safe': True,
        'parallel_write_safe': True,
        }
