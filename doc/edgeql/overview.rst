.. _ref_edgeql_overview:

Overview
========

EdgeQL is the primary language used to interact with EdgeDB, and
can be used to define, mutate and query data.  EdgeQL input consists
of a sequence of *commands*, and the database returns a specific response
to each command in sequence.

For example, the following EdgeQL ``SELECT`` command would return a
set of all `User` objects with the value of the ``name`` link equal to
``"Jonh"``.

.. code-block:: eql

    SELECT User FILTER User.name = 'John';


.. _ref_edgeql_fundamentals_type_system:

Type system
-----------

EdgeQL is a strongly typed language.  Every value in EdgeQL has a type,
which is determined statically from the database schema and the expression
that defines that value.


.. _ref_edgeql_fundamentals_set:

Everything is a set
-------------------

Every value in EdgeQL is viewed as a set of elements.
A set may be empty (*empty set*), contain a single element (a *singleton*),
or contain multiple elements.

.. note::
    :class: aside

    Strictly speaking, EdgeQL sets are *multisets*, as they do not require
    the elements to be unique.

A set cannot contain elements of different base types.  Mixing objects and
primitive types, as well as primitive types with different base type, is
not allowed.

Traditional relational databases deal with tables and use ``NULL`` as
a value denoting absence of data.  EdgeDB works with *sets*, so the absence of
data is just an empty set.


.. _ref_edgeql_fundamentals_references:

Set references and paths
------------------------

A *set reference* is a *name* (a simple identifier or a qualified schema name)
that represents a set of values.  It can be the name of an object type, the
name of a view, or an *expression alias* defined in a statement.

For example a reference to the ``User`` object type in the following
query will result in a set of all ``User`` objects:

.. code-block:: eql

    SELECT User;

Note, that unlike SQL no explicit ``FROM`` clause is needed.

A set reference can be an expression alias:

.. code-block:: eql

    WITH odd_numbers := {1, 3, 5, 7, 9}
    SELECT odd_numbers;

See :ref:`with block <ref_edgeql_with>` for more information on expression
aliases.

A *path expression* (or simply a *path*) is a special kind of set reference.
It represents a set of values that are reachable from a given set of nodes
via a specific path in the data graph.

For example, the following will result in a set of all names of ``Users`` who
are friends with some other user:

.. code-block:: eql

    SELECT User.friends.name;

.. _ref_edgeql_fundamentals_path_canon:

The longest common path prefixes in an expression are treated as equivalent
set references.

.. code-block:: eql

    SELECT (User.friends.first_name, User.friends.last_name)

The canonical form of the above query is:

.. code-block:: eql

    WITH UserFriends := User.friends
    SELECT (UserFriends.first_name, UserFriends.last_name)

.. glossary::

   scope
      A collection of all known set references at a certain point
      in an expression.

See :ref:`ref_edgeql_expressions_paths` for more information on path syntax.


.. _ref_edgeql_fundamentals_functional:

EdgeQL is functional
--------------------

EdgeQL is a functional language in the sense that every expression can
be represented as a composition of functions.

Consider a query:

.. code-block:: eql

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

Notably, every EdgeQL statement can be interpreted as a pipeline: subsequent
clauses use the result of the preceding clause as input.
See :ref:`ref_edgeql_statements` for more information on how statements
and clauses are interpreted.


.. _ref_edgeql_fundamentals_eval:

Expression evaluation
---------------------

For simplicity, a reference to a *function* in this section means any
EdgeQL operator, clause or an actual function.

There are two main ways a function is applied to an argument:
*element-wise* or as a *whole set*.  The way is determined by the
function declaration: arguments declared with the ``SET OF`` keyword
are passed as a whole set, arguments declared without the ``SET OF`` keyword
are passed *element-wise*.

For example, basic arithmetic :ref:`operators <ref_edgeql_expressions_elops>`
are declared as element-wise for their arguments, while aggregate functions,
such as :eql:func:`sum` or :eql:func:`count` take their input as a whole.

An expression is evaluated recursively using the following procedure:

1. :ref:`<Canonicalize ref_edgeql_fundamentals_path_canon>` all path
   expressions.

2. Make a cartesian product of all element-wise inputs.

3. Iterate over the input product tuple, and on every iteration:

    - replace set references in the expression and all subexpressions
      with the corresponding value from the input tuple;

    - compute the values of all ``SET OF`` arguments recursively;

    - apply the function and store the result.

4. Append the results of all iterations to obtain the final result.

Below is an example of element-wise multiplication:

.. code-block:: pseudo eql

    db> WITH A := {1, 2}, B := {3, 4}
    ... SELECT A * B;
    3
    4
    6
    8


An example of whole-set function:

.. code-block:: pseudo eql

    db> WITH A := {1, 2}
    ... SELECT count(A);
    2


An example of both:

.. code-block:: pseudo eql

    db> WITH A := {1, 2}, B := {3, 4}
    ... SELECT (A, count(B));
    (1, 2)
    (2, 2)

Importantly, when the element-wise input is iterated over, *all* set
references are replaced with a corresponding element, so when the below
expression is evaluated, ``count(A)`` is essentially ``count({a})`` and
is always equal to ``1``:

.. code-block:: pseudo eql

    db> WITH A := {1, 2}, B := {3, 4, 5}
    ... SELECT (A, count(A), count(B));
    (1, 1, 3)
    (2, 1, 3)
