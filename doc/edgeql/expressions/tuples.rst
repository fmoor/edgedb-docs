:orphan:

.. _ref_eql_expr_tuple_ctor:

Tuple Constructor
=================

A tuple constructor is an expression that consists of a sequence of
comma-separated expressions enclosed in parentheses.  It produces a
tuple value:

.. code-block:: pseudo-eql

    ( <expr> [, ... ] )

Named tuples are created using the following syntax:

.. code-block:: pseudo-eql

    ( <identifier> := <expr> [, ... ] )

Note that *all* elements in a named tuple must have a name.

A tuple constructor automatically creates a corresponding
:eql:type:`std::tuple` type:

.. code-block:: pseudo-eql

    db> SELECT ('foo', 42).__type__.name;
    std::tuple<std::str, std::int64>


.. _ref_eql_expr_tuple_elementref:

Tuple Element Reference
=======================

An element of a tuple can be referenced in the form:

.. code-block:: pseudo-eql

    <expr>.<element-index>

Here, *expr* is any expression that has a tuple type, and *element-name* is
either the *zero-based index* of the element, if the tuple is unnamed, or
the name of an element in a named tuple.

Examples:

.. code-block:: pseudo-eql

    db> SELECT (1, 'EdgeDB').0;
    {1}

    db> SELECT (number := 1, name := 'EdgeDB').name;
    {"EdgeDB"}

Referencing a non-existent tuple element will result in an error:

.. code-block:: pseudo-eql

    db> SELECT (1, 2).5;
    EdgeQLError: 5 is not a member of a tuple

    ---- query context ----

        line 1
            > SELECT (1, 2).3;
