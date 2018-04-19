from . import eql
from . import eschema
from . import graphql


def setup(app):
    eql.setup_domain(app)
    eschema.setup_domain(app)
    graphql.setup_domain(app)
