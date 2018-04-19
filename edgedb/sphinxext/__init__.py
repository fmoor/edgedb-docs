from docutils import nodes as d_nodes
from sphinx import transforms as s_transforms

from . import eql
from . import eschema
from . import graphql
from . import shared


class BlockquoteTransform(s_transforms.SphinxTransform):

    default_priority = 1  # before ReferencesResolver

    def apply(self):
        bqs = list(self.document.traverse(d_nodes.block_quote))
        if bqs:
            raise shared.EdgeSphinxExtensionError(
                f'block_quote found: {bqs[0].asdom().toxml()!r}')


def setup(app):
    eql.setup_domain(app)
    eschema.setup_domain(app)
    graphql.setup_domain(app)

    app.add_transform(BlockquoteTransform)
