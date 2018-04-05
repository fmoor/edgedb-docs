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
- A *shape annotation*
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

Set constructor
---------------

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
