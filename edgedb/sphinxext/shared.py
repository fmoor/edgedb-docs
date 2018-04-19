from docutils import nodes as d_nodes
from docutils import utils as d_utils
from docutils.parsers.rst import roles as d_roles


class InlineCodeRole:

    def __init__(self, lang):
        self.lang = lang

    def __call__(self, role, rawtext, text, lineno, inliner,
                 options={}, content=[]):
        d_roles.set_classes(options)
        node = d_nodes.literal(rawtext, d_utils.unescape(text), **options)
        node['eql-lang'] = self.lang
        return [node], []
