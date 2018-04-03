.. _ref_eql_expr:


Expressions
===========

Expressions are used to represent a *value* or a *set of values* in EdgeQL
commands.

An expression is one of the following:

- A :ref:`scalar literal <ref_eql_expr_index_literal>`
- A :ref:`set reference <ref_eql_expr_index_setref>`
- A :ref:`path <ref_eql_expr_index_path>`
- A :ref:`shape annotation <ref_eql_expr_index_shape>`
- A :ref:`parameter reference <ref_eql_expr_index_param>`
- An :ref:`operator expression <ref_eql_expr_index_operator>`
- A function call
- A type cast
- A set constructor
- A tuple constructor
- A tuple element reference
- An array constructor
- An array element reference or an array slice
- A statement in parentheses
- Any expression in parentheses (parentheses are useful for
  grouping and explicit precedence)


.. _ref_eql_expr_index_literal:

Scalar Literals
---------------

A literal representation of a supported scalar type.
See :ref:`this section <ref_eql_lexical_const>` for details about
the syntax for standard scalar literals.

Additionally, any scalar value may be represented as a casted string literal:

.. code-block:: pseudo-eql

    <float>'1.23'


.. _ref_eql_expr_index_setref:

Set References
--------------

A set reference is an *name* (a simple identifier or a qualified schema name)
that represents a set of values.  It can be the name of an object type, the
name of a view, or an *alias* defined in a statement.

For example, in the following query ``User`` is a set reference:

.. code-block:: eql

    SELECT User;

See :ref:`this section <ref_eql_fundamentals_references>` for more
information about set references.


.. _ref_eql_expr_index_path:

Paths
-----

Path expression syntax and semantics are described in a
:ref:`dedicated section <ref_eql_expr_paths>`.


.. _ref_eql_expr_index_shape:

Shapes
------

See :ref:`this section <ref_eql_expr_shapes>` for information on
shape syntax and semantics.


.. _ref_eql_expr_index_param:

Parameter References
--------------------

A parameter reference is used to indicate a value that is supplied externally
to an EdgeQL expression.  Parameter references are used in parametrized
statements and function definitions.  The form of a parameter reference is:

.. code-block:: pseudo-eql

    $name


For example, in the following function definition, ``$n`` references the
value of the function argument whenever the function is called:

.. code-block:: eql

    CREATE FUNCTION square($n: int64) -> int64 FROM EDGEQL $$
        SELECT $n * $n;
    $$;


.. _ref_eql_expr_index_operator:

Operators
---------

Most operators in EdgeQL are *binary infix* or *unary prefix* operators.
Some operators have dedicated syntax, like the :eql:op:`IF..ELSE` operator.

Binary infix operator syntax:

.. code-block:: pseudo-eql

    <expression> <operator> <expression>

Unary prefix operator syntax:

.. code-block:: pseudo-eql

    <operator> <expression>

A complete reference of EdgeQL operators can be found in
:ref:`ref_eql_funcop`.


.. _ref_eql_expr_index_typecast:

Type Casts
----------

A type cast expression converts the specified value to another value of
the specified type:

.. code-block:: eql

    "<" <type> ">" <expression>

The *type* must be a scalar or a container type.

For example, the following expression casts an integer value into a string:

.. code-block:: pseudo-eql

    db> SELECT <str>10;
    {"10"}

See :ref:`type cast reference <ref_eql_expr_typecast>` for more
information on type casting rules.


.. _ref_eql_expr_index_set_ctor:

Set Constructor
---------------

A *set constructor* is an expression that consists of a sequence of
comma-separated expressions enclosed in curly braces:

.. code-block:: pseudo-eql

    { <expr> [, ...] }

A set constructor produces the result by appending its elements.  It is
perfectly equivalent to a sequence of :eql:op:`UNION` operators.

An *empty set* can also be created by omitting all elements.
In situations where EdgeDB cannot infer the type of an empty set,
it must be used together with a type cast:

.. code-block:: pseudo-eql

    db> SELECT {};
    EdgeQLError: could not determine the type of empty set

    db> SELECT <int>{};
    {}


Array constructor
-----------------

.. TODO



Statements
----------

Any ``SELECT`` or ``FOR`` statement, and, with some restrictions, ``INSERT``,
``UPDATE`` or ``DELETE`` statements may be used as expressions.  Parentheses
are required around the statement to disambiguate:

.. code-block:: eql

    1 + (SELECT len(User.name))

For more information about statements refer to
:ref:`this section <ref_eql_statements>`.
