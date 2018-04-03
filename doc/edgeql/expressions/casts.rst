:orphan:

.. _ref_eql_expr_typecast:

Type Casts
----------

A type cast expression converts the specified value to another value of
the specified type:

.. code-block:: pseudo-eql

    "<" <type> ">" <expression>

The *type* must be a scalar or a container type.

Type cast is a run-time operation.  The cast will succeed only if a
type conversion was defined for the type pair, and if the source value
satisfies the requirements of a target type.

EdgeDB allows casting any scalar

When a cast is applied to an expression of a known type, it represents a
run-time type conversion. The cast will succeed only if a suitable type
conversion operation has been defined.
