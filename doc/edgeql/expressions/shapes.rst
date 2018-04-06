:orphan:

.. _ref_eql_expr_shapes:

Shapes
======

A *shape* is a powerful syntactic construct that can be used to dynamically
describe a data graph.  Shapes are used to describe ``views``, ``insert`` and
``update`` data and to specify the format of statement output.

Shapes always follow an expression, and are a list of *shape elements*
enclosed in curly braces:

.. code-block:: pseudo-eql

    <expr> {
        <shape_element> [, ...]
    }


Shape element has the following syntax:

.. code-block:: pseudo-eql

    [ "[" IS <object-type> "]" ] <pointer-spec>

If an optional type filter is used, *pointer-spec* will only apply to
those objects in the *expr* set that are instances of *object-type*.

*pointer-spec* is one of the following:

- a name of an existing link or link property of a type produced
  by *expr*;

- a declaration of a computable link or link property in the form
  ``[@]<name> := <ptrexpr>``;

- a *subshape* in the form ``<link>: [<target-type>]{ ... }``, where *link* is
  the name of an existing link, and *target-type* is an optional object type
  that specifies the type of target objects selected or inserted, depending
  on the context.


Shapes in INSERT
----------------

A shape in an ``INSERT`` statement is used to specify the data to insert
into a database.  The recursive nature of shapes allows creating an entire
tree of objects with a single ``INSERT`` statement.

.. code-block:: edgeql

    INSERT Issue {
        name := 'Issue #1',
        comments: Comment {
            body := 'Issue #1 created'
        }
    };

The above query inserts a new ``Issue`` object, and creates and links a new
``Comment`` object to it.

See :ref:`ref_eql_statements_insert` for more information on the use of
shapes in ``INSERT`` statements.


Shapes in UPDATE
----------------


Shapes in queries
-----------------

A shape in a ``SELECT`` clause (or the ``UNION`` clause of a
``FOR`` statement) determines the output format for the objects in a set
computed by an expression annotated by the shape.

For example, the below query returns a set of ``Issue`` objects and includes
a ``number`` and an associated owner ``User`` object, which in turn includes
the ``name`` and the ``email`` for that user.

.. code-block:: pseudo-eql

    db> SELECT
    ...     Issue {
    ...         number,
    ...         owner: {  # sub-shape, selects Issue.owner objects
    ...            name,
    ...            email
    ...         }
    ...     };

    {
        'number': 1,
        'owner': {
            'name': 'Alice',
            'email': 'alice@example.com'
        }
    }

.. TODO: old content below, rework and incorporate more examples.

.. _ref_eql_shapes:

Shapes
------

Shapes are a way of specifying which data should be retrieved for each
object. This annotation does not actually alter the objects in any
way, but rather provides a guideline for serialization.

Shapes define the *relationships structure* of the data that is
retrieved from the DB. Thus shapes themselves are a lexical
specification used with valid expressions denoting objects.

Shapes allow retrieving a set of objects as a `forest`, where each
base object is the root of a `tree`. Technically, this set of trees is
a directed graph possibly even containing cycles. However, the
serialized representation is based on a set of trees (or nested JSON).

Another use of shapes is *augmentation* of the object data. This can
be useful for serialization, but also as a convenient way of computing
some values used for filtering.

For example it's possible to augment each user object with the
information about how many issues they have:

.. code-block:: edgeql

    SELECT User {
        name,
        # "issues" is not a link in the schema, it is a computable
        # defined in the shape
        issues := count(User.<owner[IS Issue])
    };

Similarly, we can add a filter based on the number of issues that a
user has by referring to the :ref:`computable<ref_eql_computables>`
defined by the shape:

.. code-block:: edgeql

    SELECT User {
        name,
        issues := count(User.<owner[IS Issue])
    } FILTER User.issues > 5;

In order to refer to :ref:`computables<ref_eql_computables>` a
shape must be in the same lexical statement as the expression
referring to it.

.. note::

    Shapes serve an important function of pre-fetching specific data
    and *that data only* when serialized. For example, it's possible
    to fetch all issues with ``watchers`` restricted to a specific
    subset of users, then in the processing code safely refer to
    ``issue.watchers`` without further restrictions and only access
    the restricted set of watchers that was fetched.

    .. code-block:: edgeql

        SELECT Issue {
            name,
            text,
            # we only want real watchers, not internal
            # system accounts
            watchers: {
                name
            } FILTER Issue.watchers IS NOT SystemUser
        };


Using shapes
------------

:ref:`Shapes<ref_eql_shapes>` are the way of specifying structured
object data. They are used to get a set of ``objects`` and their
relationships in a structured way. Shape specification can be added to
any expression that denotes an object. Fundamentally, a shape
specification does not alter the identity of the objects it is
attached to, because it doesn't in any way change the existing
objects, but rather specifies additional data about them.

For example, a query that retrieves a set of ``Issue`` objects with
``name`` and ``body``, but no other information (like
``time_estimate``, ``owner``, etc.) for all of the issues owned by
Alice Smith, would look like this:

.. code-block:: edgeql

    WITH MODULE example
    SELECT
    Issue {
        name,
        body
    } FILTER Issue.owner.name = 'Alice Smith';

Shapes can be nested to retrieve more complex structures:

.. code-block:: edgeql

    WITH MODULE example
    SELECT Issue {  # base shape
        name,
        body,
        owner: {    # this is a nested shape
            name
        }
    };

The above query will retrieve all of the ``Issue`` objects. Each
object will have ``name``, ``body`` and ``owner`` links, where
``owner`` will also have a ``name``. To restrict this to only issues
that are not 'closed', the following query can be used:

.. code-block:: edgeql

    WITH MODULE example
    SELECT Issue {  # base shape
        name,
        body,
        owner: {    # this is a nested shape
            name
        }
    } FILTER Issue.status.name != 'closed';


To retrieve all users and their associated issues (if any), the following
shape query can be used:

.. code-block:: edgeql

    WITH MODULE example
    SELECT User {
        name,
        owned := (SELECT
            User.<owner[IS Issue] {
                number,
                body,
                status: {
                    name
                }
            }
        )
    };

By default only outbound links may be referred to in shapes directly
(like link ``status`` for the concept ``Issue``). Thus a computable
``owned`` is used to include data by following the inbound link
``owner`` to its origin. Since the link ``owner`` on ``Issue`` is
``*1`` (by default), when it is followed in the other direction is
functions as a ``1*``. So ``<owner`` points to a ``set`` of multiple
issues sharing a particular owner. For each issue the sub-shape for
the ``status`` link will be retrieved containing just the ``name``.

Note that the the sub-shape does not mandate that only the users that
*own* at least one ``Issue`` are returned, merely that *if* they have
some issues the names and bodies of these issues should be included in
the returned value. The query effectively says 'please return the set
of *all* users and provide this specific information for each of them
if available'. This is one of the important differences between
``shape`` specification and a :ref:`path <ref_eql_expr_paths>`.

Shape annotation is preserved only by operations that preserve the
type (rather than specify a type or the result explicitly). In general
terms, any operation that maps :eql:type:`any` onto :eql:type:`any`
also preserves shapes, but operations that specify the types
explicitly (such as :eql:op:`+<PLUS>`, which is polymorphic, but
specifies :eql:type:`int64`, :eql:type:`float64`, or :eql:type:`str`
explicitly as the return type) effectively "remove" shape annotation
from the result.
