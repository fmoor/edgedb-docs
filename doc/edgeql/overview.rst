.. _ref_eql_overview:

========
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

Type System
===========

EdgeQL is a strongly typed language.  Every value in EdgeQL has a type,
which is determined statically from the database schema and the expression
that defines that value.  Refer to
:ref:`Data Model <ref_datamodel_typesystem>` for details about the type
system.


.. _ref_eql_fundamentals_set:

Everything is a Set
===================

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

In SQL databases ``NULL`` is a special *value* denoting an absence of data.
EdgeDB works with *sets*, so an absence of data is just an empty set.
See :ref:`ref_eql_emptyset` on how empty sets are handled.


.. _ref_eql_fundamentals_references:

Set References and Paths
========================

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
sequence of links or properties from some source set.

For example, the following will result in a set of all names of ``Users`` who
are friends with some other user:

.. code-block:: edgeql

    SELECT User.friends.name;

When two or more paths in an expression share a common prefix
(i.e. start the same), then their longest common path prefix is treated
as an equivalent set reference

.. code-block:: edgeql

    SELECT (User.friends.first_name, User.friends.last_name);

The canonical form of the above query is:

.. code-block:: edgeql

    WITH UserFriends := User.friends
    SELECT (UserFriends.first_name, UserFriends.last_name);


See :ref:`ref_eql_expr_paths` for more information on path syntax and
behavior.


.. _ref_eql_fundamentals_aggregates:

Aggregates
==========

A function parameter or an operand of an operator can be declared as
*aggregate parameter*.  An aggregate parameter means that the function or
operator are called *once* on an entire set passed as a corresponding
argument, rather than being called sequentially on each element of an
argument set.  A function or an operator with an aggregate parameter is
called an *aggregate*.  Non-aggregate functions and operators are
*regular* functions and operators.

For example, basic arithmetic :ref:`operators <ref_eql_funcop_math>`
are regular operators, while the :eql:func:`sum` function and the
:eql:op:`IN` operator are aggregates.

An aggregate parameter is normally specified using the ``SET OF`` modifier
in the function declaration.  See :eql:stmt:`CREATE FUNCTION` for details.


.. _ref_eql_fundamentals_queries:

Queries
=======

EdgeQL is a functional language in the sense that every expression is
a composition of one or more queries.  A *query* is an expression that
produces a set of values and is evaluated according to the algorithm below.
A nested query is called a *subquery*.

Subqueries can be *explicit*, such as a :eql:stmt:`SELECT` statement,
or *implicit*, as dictated by the semantics of a function, operator or
a statement clause.

An implicit ``SELECT`` subquery is assumed in the following situations:

- expressions passed as an argument for an aggregate function parameter
  or operand;

- the right side of turnstile (``:=``) in expression aliases and
  :ref:`shape element declarations <ref_eql_expr_shapes>`;

- the majority of statement clauses;

- any set returning function or operator (e.g. a :ref:`set constructor
  <ref_eql_expr_index_set_ctor>`).

.. _ref_eql_fundamentals_eval_algo:

A query is evaluated recursively using the following procedure:

1. Replace all common path prefixes in a query and all its subqueries
   with equivalent set references.

2. Make a cartesian product of all unique set references appearing
   directly in the query (not in the subqueries). The result of the
   product is a set of *input tuples*. If there are no set references
   appearing directly in the main query, take the input set to contain
   a single empty tuple. See :ref:`ref_eql_emptyset` on what happens
   when the product is empty.

3. Iterate over the input tuple set, and on every iteration:

   - replace set references in the query and all its subqueries
     with the corresponding value from the input tuple;

   - compute the values of all subqueries and function calls, and treat
     the results as set references;

   - make another cartesian product from the input tuple and the
     sets produced by subqueries and functions, excluding the sets
     used as aggregate arguments;

   - for every element of the nested cartesian product, compute
     the value of the query and store the result.

4. Append the results of all iterations to obtain the final result set.


.. _ref_eql_emptyset:

Empty Set Handling
==================

In the :ref:`evaluation algorithm <ref_eql_fundamentals_eval_algo>` above,
the second step is making a cartesian product of element-wise inputs.
Consequently, if any argument is an *empty set* the product will also be an
empty set.  In this situation there are two possible scenarios:

1. If *none* of the functions in the query have arguments declared as
   ``OPTIONAL``, the result is an empty set.  This is the most common case.

2. If *any* of the functions in the query have arguments declared as
   ``OPTIONAL``, these functions are called as usual, with arguments
   passed as empty sets.

For example, the following query returns an empty set:

.. code-block:: edgeql-repl

    db> SELECT {2} * {};
    {}

A notable example of a function that *does* get called on empty input
is the :eql:op:`coalescing <COALESCE>` operator.
