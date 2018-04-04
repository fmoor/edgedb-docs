.. _ref_edgeql_expressions:


Expressions
===========

Expressions are used to represent a *value* or a *set of values* in EdgeQL
commands.

An expression is one of the following:

- A :ref:`scalar literal <ref_edgeql_lexical_const`
- A parameter reference
- A set reference
- A *path*
- A *shape*
- An operator expression
- A function call
- A type cast
- A set constructor
- A tuple constructor
- A tuple element reference
- An array constructor
- A subscripted expression
- A statement in parentheses
- Any expression in parentheses (parentheses are useful for
  grouping and explicit precedence)


Set references
--------------

A set reference is an *name* (a simple identifier or a qualified schema name)
that represents a set of values.  It can be the name of an object type, the
name of a view, or an *alias* defined in a statement.

.. _ref_edgeql_expressions_paths:

Paths
-----

A *path expression* (or simply a *path*) represents a set of values that
can be reached from a given set of source nodes by navigating a specific
path in the data graph.  The form of a path is:

.. code-block:: pseudo-eql

    expression path-step [ path-step ... ]

Here *expression* is any expression and *path-step* is:

.. code-block:: pseudo-eql

    step-direction pointer-name [ step-target-filter ]

*step-direction* is one of the following:

- ``.`` or ``.>`` for an outgoing link reference
- ``.<`` for an incoming link reference
- ``@`` for a link property reference

*pointer-name* must be a valid link or link property name.

*step-target-filter* is an optional filter that narrows which *types* of
objects should be included in the result.  It has the following syntax:

.. code-block:: pseudo-eql

   [ IS type ]

The example below shows a path that represents the names of all friends
of all ``User`` objects in the database.

.. code-block:: eql

    User.friends.name

And this represents all users who are owners of at least one ``Issue``:

.. code-block:: eql

    Issue.<owners[IS User]

And this represents a set of all dates on which users became friends,
if ``since`` is defined as a link property on the ``User.friends`` link:

.. code-block:: eql

    User.friends@since

.. note::

    Link properties cannot point to objects, hence the ``@`` indirection
    will always be the last step in a path.


Shapes
------

Shapes are a way to specify entire sets of trees in the data graph.
The first element of the shape is the `root` of the tree. The nested
structure consists of various legally reachable links.

.. code-block:: eql

    WITH MODULE example
    SELECT
        # everything below is a shape
        Issue {  # root
            number,
            owner: {  # sub-shape
                name,
                email
            }
        };

One big difference between shapes and path expressions is that any
non-root shape element is optional. This means that every tree denoted
by a shape must start at the shape's root and be the largest reachable
tree given the hierarchy of links in the shape.

For a complete description of shapes refer to
:ref:`this section <ref_edgeql_shapes>`.


Operator expressions
--------------------

There are *binary infix* and *unary prefix* operators in EdgeQL.

Binary infix operator syntax:

.. code-block:: pseudo-eql

    expression operator expression

Unary prefix operator syntax:

.. code-block:: pseudo-eql

    operator expression

For a complete reference of EdgeQL operators refer to
:ref:`this section <ref_edgeql_operators>`.


Function calls
--------------

The syntax for a function call is as follows:

.. code-block:: pseudo-eql

    function_name ([argument [, argument ...]])

Here *function_name* is a possibly qualified name of a function, and
*argument* is an *expression* optionally prefixed with an argument name
and a turnstile (``:=``).

For example, the following computes the length of a string ``'foo'``:

.. code-block:: eql

    len('foo')

For more information on functions refer to
:ref:`this section <ref_edgeql_functions>`.


Type casts
----------

A type cast expression converts the specified value to another value of
the specified type:

.. code-block:: eql

    <type>expression

The *type* must be a scalar or a container type.


Set constructor
---------------

.. TODO


.. _ref_edgeql_expressions_tuple_constructor:

Tuple constructor
-----------------

.. TODO

Creating collections syntactically (e.g. using ``[...]`` or ``(...)``)
is an element-wise operation. One way of thinking about these syntax
constructs is to treat them exactly like functions that simply turn
their arguments into a set of collections.

This means that the following code will create a set of tuples with
the first element being ``Issue`` and the second a :eql:type:`str`
representing the ``Issue.priority.name``:

.. code-block:: eql

    WITH MODULE example
    SELECT (Issue, Issue.priority.name);

Since ``priority`` is not a required link, not every ``Issue`` will
have one. It is important to realize that the above query will *only*
contain Issues with non-empty priorities. If it is desirable to have
*all* Issues, then coalescing (:eql:op:`??<COALESCE>`) or a
:ref:`shape<ref_edgeql_shapes>` query should be used instead.

On the other hand the following query will include *all* Issues,
because the tuple elements are made from the set of Issues and the set
produced by the aggregate function :eql:func:`array_agg`, which is
never ``{}``:

.. code-block:: eql

    WITH MODULE example
    SELECT (Issue, array_agg(Issue.priority.name));


Tuple element reference
-----------------------

.. TODO


Array constructor
-----------------

.. TODO


Subscripts
----------

.. TODO


Statements
----------

Any ``SELECT`` or ``FOR`` statement, and, with some restrictions, ``INSERT``,
``UPDATE`` or ``DELETE`` statements may be used as expressions.  Parentheses
are required around the statement to disambiguate:

.. code-block:: eql

    1 + (SELECT len(User.name))

For more information about statements refer to
:ref:`this section <ref_edgeql_statements>`.


Expression evaluation rules
---------------------------

.. TODO
