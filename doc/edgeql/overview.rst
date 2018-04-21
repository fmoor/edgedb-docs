.. _ref_eql_overview:

Overview
========

EdgeQL is the primary language of EdgeDB.  It is used to define, mutate, and
query data.

EdgeQL input consists of a sequence of *commands*, and the database
returns a specific response to each command in sequence.

For example, the following EdgeQL :eql:stmt:`SELECT` command would return a
set of all ``User`` objects with the value of the ``name`` property equal to
``"John"``.

.. code-block:: edgeql

    SELECT User FILTER User.name = 'John';


.. _ref_eql_fundamentals_type_system:

Type system
-----------

EdgeQL is a strongly typed language.  Every value in EdgeQL has a type,
which is determined statically from the database schema and the expression
that defines that value.  Refer to :ref:`Data Model <ref_datamodel_overview>`
for details about the type system.


.. _ref_eql_fundamentals_set:

Everything is a Set
-------------------

Every value in EdgeQL is viewed as a set of elements.  A set may be empty
(*empty set*), contain a single element (a *singleton*), or contain multiple
elements.

.. note::
    :class: aside

    Strictly speaking, EdgeQL sets are *multisets*, as they do not require
    the elements to be unique.

A set cannot contain elements of different base types.  Mixing objects and
primitive types, as well as primitive types with different base type, is
not allowed.

In SQL databases ``NULL`` is a special *value* denoting the absence of data.
EdgeDB works with *sets*, so the absence of data is just an empty set.


.. _ref_eql_fundamentals_functional:

EdgeQL is Functional
--------------------

EdgeQL is a functional language in the sense that every expression can
be represented as a composition of functions.

Consider a query:

.. code-block:: edgeql

    SELECT User
    FILTER User.age > 20
    ORDER BY User.name;

EdgeDB will evaluate this query as the following hypothetical functional
expression:

::

    order(
        filter(
            select_all(type = 'User'),
            predicate = function(u) => greater(u.age, 20)
        ),
        key = function(u) => u.name
    )

See :ref:`ref_eql_eval` on general EdgeQL expression evaluation rules.


.. _ref_eql_fundamentals_references:

Set References and Paths
------------------------

A *set reference* is a *name* (a simple identifier or a qualified schema name)
that represents a set of values.  It can be the name of an object type, the
name of a view, or an *expression alias* defined in a statement.

For example a reference to the ``User`` object type in the following
query will result in a set of all ``User`` objects:

.. code-block:: edgeql

    SELECT User;

Note, that unlike SQL no explicit ``FROM`` clause is needed.

A set reference can be an expression alias:

.. code-block:: edgeql

    WITH odd_numbers := {1, 3, 5, 7, 9}
    SELECT odd_numbers;

See :ref:`with block <ref_eql_with>` for more information on expression
aliases.

A *path expression* (or simply a *path*) is a special kind of set reference.
It represents a set of values that are reachable when traversing a given
sequence of links or link properties from some source set.

For example, the following will result in a set of all names of ``Users`` who
are friends with some other user:

.. code-block:: edgeql

    SELECT User.friends.name;

.. _ref_eql_fundamentals_path_canon:

When two or more paths in an expression share a common prefix
(i.e. start the same), then their longest common path prefix is treated
as an equivalent set reference

.. code-block:: edgeql

    SELECT (User.friends.first_name, User.friends.last_name)

The canonical form of the above query is:

.. code-block:: edgeql

    WITH UserFriends := User.friends
    SELECT (UserFriends.first_name, UserFriends.last_name)


See :ref:`ref_eql_expr_paths` for more information on path syntax and
behavior.
