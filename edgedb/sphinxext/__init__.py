"""
=====================================
:eql: domain for EdgeQL documentation
=====================================


Functions
---------

To declare a function use a ".. eql:function::" directive.  A few
things must be defined:

* Full function signature with a fully qualified name must be specified.

* ":param $name: description:" a short description of the $name parameter.
  $name must match the the name of the parameter in function's signature.
  If a parameter is anonymous, its number should be used instead (e.g. $1).

* ":paramtype $name: type": for every :param: there must be a
  corresponding :paramtype field.  For example: ":paramtype $name: int"
  declares that the type of the $name parameter is `int`.  If a parameter
  has more than one valid types list them separated by "or":
  ":paramtype $name: int or str".

* :return: and :returntype: are similar to :param: and
  :paramtype: but lack parameter names.  They must be used to document
  the return value of the function.

* A few paragraphs and code samples.  The first paragraph must
  be a single sentence no longer than 79 characters describing the
  function.

Example::

    .. eql:function:: std::array_agg(SET OF any, $a: any) -> array<any>
        :param $1: input set
        :paramtype $1: SET OF any

        :param $a: description of this param
        :paramtype $a: int or str

        :return: array made of input set elements
        :returntype: array<any>

        Return the array made from all of the input set elements.

        The ordering of the input set will be preserved if specified.


A function can be referenced from anywhere in the documentation by using
a ":eql:func:" role.  For instance:

* ":eql:func:`std::array_agg`";
* or, "look at this :eql:func:`fancy function <std::array_agg>`".

"""


import re

from edgedb.lang.edgeql.pygments import EdgeQLLexer
from edgedb.lang.graphql.pygments import GraphQLLexer
from edgedb.lang.schema.pygments import EdgeSchemaLexer

from edgedb.lang.edgeql.parser import parser as edgeql_parser
from edgedb.lang.edgeql import ast as ql_ast
from edgedb.lang.edgeql import codegen as ql_gen

from docutils import nodes as d_nodes

from sphinx import addnodes as s_nodes
from sphinx import directives as s_directives
from sphinx import domains as s_domains
from sphinx import roles as s_roles
from sphinx.util import docfields as s_docfields
from sphinx.util import nodes as s_nodes_utils


class EQLField(s_docfields.Field):

    def make_field(self, *args, **kwargs):
        node = super().make_field(*args, **kwargs)
        node['name'] = self.name
        return node

    def make_xrefs(self, rolename, domain, target, innernode=d_nodes.emphasis,
                   contnode=None, env=None):
        delims = r'(\s*[\[\]\(\),](?:\s*or\s)?\s*|\s+or\s+)'
        delims_re = re.compile(delims)
        sub_targets = re.split(delims, target)

        split_contnode = bool(contnode and contnode.astext() == target)

        results = []
        for sub_target in filter(None, sub_targets):
            if split_contnode:
                contnode = d_nodes.Text(sub_target)

            if delims_re.match(sub_target):
                results.append(contnode or innernode(sub_target, sub_target))
            else:
                results.append(self.make_xref(rolename, domain, sub_target,
                                              innernode, contnode, env))

        return results


class EQLTypedField(EQLField):

    is_typed = True

    def __init__(self, name, names=(), label=None, rolename=None,
                 typerolename=None, typenames=(), has_arg=True):
        super().__init__(name, names, label, has_arg, rolename)
        self.typenames = typenames
        self.typerolename = typerolename

    def make_field(self, types, domain, item, env=None):
        fieldname = d_nodes.field_name('', self.label)

        fieldarg, content = item
        body = d_nodes.paragraph()
        body.extend(self.make_xrefs(self.rolename, domain, fieldarg,
                                    s_nodes.literal_strong, env=env))

        typename = None
        if fieldarg in types:
            body += d_nodes.Text(' (')

            # NOTE: using .pop() here to prevent a single type node to be
            # inserted twice into the doctree, which leads to
            # inconsistencies later when references are resolved
            fieldtype = types.pop(fieldarg)
            if len(fieldtype) == 1 and isinstance(fieldtype[0], d_nodes.Text):
                typename = u''.join(n.astext() for n in fieldtype)
                body.extend(
                    self.make_xrefs(self.typerolename, domain, typename,
                                    s_nodes.literal_emphasis, env=env))
            else:
                body += fieldtype
            body += d_nodes.Text(')')

        body += d_nodes.Text(' -- ')
        body += content

        fieldbody = d_nodes.field_body('', body)

        node = d_nodes.field('', fieldname, fieldbody)
        node['name'] = self.name
        node['paramname'] = fieldarg
        if typename:
            node['paramtype'] = typename
        return node


class DirectiveParseError(Exception):
    def __init__(self, directive, msg, *, cause=None):
        fn, lineno = directive.state_machine.get_source_and_line()
        msg = f'{msg} in {fn}:{lineno}'
        if cause is not None:
            msg = f'{msg}\nCause: {type(cause).__name__}\n{cause}'
        super().__init__(msg)


class BaseEQLDirective(s_directives.ObjectDescription):

    def run(self):
        indexnode, node = super().run()

        desc_cnt = None
        for child in node.children:
            if isinstance(child, s_nodes.desc_content):
                desc_cnt = child
                break
        if desc_cnt is None or not desc_cnt.children:
            raise DirectiveParseError(
                self, 'the directive must include a description')

        first_node = desc_cnt.children[0]
        if isinstance(first_node, d_nodes.field_list):
            if len(desc_cnt.children) < 2:
                raise DirectiveParseError(
                    self, 'the directive must include a description')

            first_node = desc_cnt.children[1]

        if not isinstance(first_node, d_nodes.paragraph):
            raise DirectiveParseError(
                self,
                'there must be a short text paragraph after directive fields')

        summary = first_node.astext().strip()
        summary = ' '.join(
            line.strip() for line in summary.split() if line.strip())

        if len(summary) > 79:
            raise DirectiveParseError(
                self,
                f'First paragraph is expected to be shorter than 80 '
                f'characters, got {len(summary)}: {summary!r}')

        node['summary'] = summary
        return [indexnode, node]


class EQLFunctionDirective(BaseEQLDirective):

    doc_field_types = [
        EQLTypedField(
            'parameter',
            label='Parameter',
            names=('param',),
            typerolename='type',
            typenames=('paramtype',)),

        EQLTypedField(
            'return',
            label='Return',
            names=('return',),
            has_arg=False,
            typerolename='type',
            typenames=('returntype',)),
    ]

    def handle_signature(self, sig, signode):
        parser = edgeql_parser.EdgeQLBlockParser()
        try:
            astnode = parser.parse(
                f'CREATE FUNCTION {sig} FROM SQL FUNCTION "xxx";')[0]
        except Exception as ex:
            raise DirectiveParseError(
                self, f'could not parse function signature {sig!r}',
                cause=ex)

        if (not isinstance(astnode, ql_ast.CreateFunction) or
                not isinstance(astnode.name, ql_ast.ClassRef)):
            raise DirectiveParseError(
                self, f'EdgeQL parser returned unsupported AST')

        modname = astnode.name.module
        funcname = astnode.name.name

        if not modname:
            raise DirectiveParseError(
                self, f'EdgeQL function declaration is missing namespace')

        signode['eql-module'] = modname
        signode['eql-name'] = funcname
        signode['eql-fullname'] = fullname = f'{modname}::{funcname}'

        signode += s_nodes.desc_name(fullname, fullname)

        params = s_nodes.desc_parameterlist()
        for idx, param in enumerate(astnode.args):
            name = param.name
            if not name:
                name = f'${idx}'

            param_repr = ql_gen.EdgeQLSourceGenerator.to_source(param)
            param_node = s_nodes.desc_parameter(param_repr, param_repr)
            param_node['eql-name'] = name
            params += param_node
        signode += params

        ret_repr = ql_gen.EdgeQLSourceGenerator.to_source(astnode.returning)
        signode += s_nodes.desc_returns(ret_repr, ret_repr)

        return fullname

    def add_target_and_index(self, name, sig, signode):
        if name in self.state.document.ids:
            raise DirectiveParseError(
                self, f'duplicate function {name} description')

        signode['names'].append(name)
        signode['ids'].append(name)
        signode['first'] = (not self.names)
        self.state.document.note_explicit_target(signode)

        objects = self.env.domaindata['eql']['objects']
        if name in objects:
            raise DirectiveParseError(
                self, f'duplicate function {name} description')
        objects[name] = (self.env.docname, self.objtype)


class EdgeQLDomain(s_domains.Domain):

    name = "eql"
    label = "EdgeQL"

    object_types = {
        'function': s_domains.ObjType('function', 'func'),
    }

    directives = {
        'function': EQLFunctionDirective,
    }

    roles = {
        'func': s_roles.XRefRole(),
    }

    initial_data = {
        'objects': {}  # fullname -> docname, objtype
    }

    def resolve_xref(self, env, fromdocname, builder,
                     type, target, node, contnode):

        objects = self.data['objects']

        if node['reftype'] == 'func':
            try:
                docname, obj_type = objects[target]
            except KeyError:
                raise DirectiveParseError(
                    self,
                    f'cannot resolve :eql:{type}: targeting {target!r}')

            node = s_nodes_utils.make_refnode(
                builder, fromdocname, docname, target, contnode, None)
            node['eql-type'] = obj_type
            return node

        return super().resolve_xref(
            env, fromdocname, builder, type, target, node, contnode)

    def clear_doc(self, docname):
        for fullname, (fn, _l) in list(self.data['objects'].items()):
            if fn == docname:
                del self.data['objects'][fullname]

    def merge_domaindata(self, docnames, otherdata):
        for fullname, (fn, objtype) in otherdata['objects'].items():
            if fn in docnames:
                self.data['objects'][fullname] = (fn, objtype)

    def get_objects(self):
        for refname, (docname, type) in self.data['objects'].items():
            yield (refname, refname, type, docname, refname, 1)

    def get_full_qualified_name(self, node):
        fn = node.get('eql-fullname')
        if not fn:
            raise DirectiveParseError(
                self, 'no eql-fullname attribute')
        return fn


def setup(app):
    app.add_lexer("eschema", EdgeSchemaLexer())
    app.add_lexer("eql", EdgeQLLexer())
    app.add_lexer("pseudo-eql", EdgeQLLexer())
    app.add_lexer("graphql", GraphQLLexer())

    app.add_domain(EdgeQLDomain)
