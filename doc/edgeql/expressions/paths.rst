:orphan:

.. _ref_eql_expr_paths:

Paths
=====

A *path expression* (or simply a *path*) is a special kind of set reference.
It represents a set of values that are reachable when traversing a given
sequence of links or link properties from some source set.

The form of a path is:

.. eql:synopsis::

    <expression> <path-step> [ <path-step> ... ]

Here :eql:synopsis:`<expression>` is any expression and
:eql:synopsis:`<path-step>` is:

.. eql:synopsis::

    <step-direction> <pointer-name> [ <step-target-filter> ]

:eql:synopsis:`<step-direction>` is one of the following:

- ``.`` or ``.>`` for an outgoing link reference
- ``.<`` for an incoming link reference
- ``@`` for a link property reference

:eql:synopsis:`<pointer-name>` must be a valid link or link
property name.

:eql:synopsis:`<step-target-filter>` is an optional filter that
narrows which :eql:synopsis:`<type>` of objects should be
included in the result.  It has the following syntax:

.. eql:synopsis::

   "[" IS type "]"

The example below shows a path that represents the names of all friends
of all ``User`` objects in the database.

.. code-block:: edgeql

    User.friends.name

And this represents all users who are owners of at least one ``Issue``:

.. code-block:: edgeql

    Issue.<owners[IS User]

And this represents a set of all dates on which users became friends,
if ``since`` is defined as a link property on the ``User.friends`` link:

.. code-block:: edgeql

    User.friends@since

.. note::

    Link properties cannot point to objects, hence the ``@`` indirection
    will always be the last step in a path.


.. _ref_eql_expr_paths_interp:

Path Interpretation
-------------------

.. TODO: incomplete

The manner in which a path expression is interpreted depends on the
expression.

When two or more paths in an expression share a common prefix
(i.e. start the same), then their longest common path prefix is treated
as an equivalent set reference

The longest common path prefixes in an expression are treated as equivalent
set references.

.. code-block:: edgeql

    SELECT (User.friends.first_name, User.friends.last_name)

The canonical form of the above query is:

.. code-block:: edgeql

    WITH UserFriends := User.friends
    SELECT (UserFriends.first_name, UserFriends.last_name)
