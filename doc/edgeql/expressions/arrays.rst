:orphan:

.. _ref_eql_expr_array_ctor:

Array Constructor
=================

An array constructor is an expression that consists of a sequence of
comma-separated expressions *of the same type* enclosed in square brackets.
It produces an array value:

.. code-block:: pseudo-eql

    "[" <expr> [, ...] "]"

For example:

.. code-block:: pseudo-eql

    db> SELECT [1, 2, 3];
    {
      [1, 2, 3]
    }

An empty array can also be created, but it must be used together with
a type case, since EdgeDB cannot determine the type of an array without
having elements in it:

.. code-block:: pseudo-eql

    db> SELECT [];
    EdgeQLError: could not determine the type of empty array

    db> SELECT <array<int>>[];
    {[]}


.. _ref_eql_expr_array_elementref:

Array Element Reference
=======================

An element of an array can be referenced in the following form:

.. code-block:: pseudo-eql

    <expr> "[" <index-expr> "]"

Here, *expr* is any expression of array type, and *index-expr* is any
integer expression.

Example:

.. code-block:: pseudo-eql

    db> SELECT [1, 2, 3][0]
    {1}

Negative indexing is supported:

.. code-block:: pseudo-eql

    db> SELECT [1, 2, 3][-1]
    {3}

Referencing a non-existent array element will result in an empty set:

.. code-block:: pseudo-eql

    db> SELECT [1, 2, 3][0]
    {}


.. _ref_eql_expr_array_slice:

Array Slice
===========

An array slice can be referenced in the following form:

.. code-block:: pseudo-eql

    <expr> "[" <lower-bound> : <upper-bound> "]"

Here, *expr* is any expression of array type, and *lower-bound* and
*upper-bound* are arbitrary integer expressions.  Both *lower-bound*,
and *upper-bound* are optional.  An ommitted *lower-bound* default to zero,
and an ommitted *upper-bound* defaults to the size of the array.
The upper bound is non-inclusive.

Examples:

.. code-block:: pseudo-eql

    db> SELECT [1, 2, 3][0:2]
    {
      [1, 2]
    }

    db> SELECT [1, 2, 3][2:]
    {
      [3]
    }

    db> SELECT [1, 2, 3][:1]
    {
      [1]
    }

    db> SELECT [1, 2, 3][:-2]
    {
      [1]
    }

Referencing a non-existent array slice will result in an empty array:

.. code-block:: pseudo-eql

    db> SELECT [1, 2, 3][10:20]
    {[]}
