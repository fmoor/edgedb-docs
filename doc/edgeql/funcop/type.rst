.. _ref_eql_funcop_type:

================
Type Expressions
================

This section describes EdgeQL expressions related to *types*.


IS
==

.. eql:operator:: IS: A IS B or A IS NOT B

    :optype A: any
    :optype B: type
    :resulttype: bool

    Type-checking of ``A`` w.r.t. type ``B``.

    Type-checking operators :eql:op:`IS` and :eql:op:`IS NOT<IS>` that
    test whether the left operand is of any of the types given by the
    comma-separated list of types provided as the right operand.

    Note that ``B`` is special and is not any kind of expression, so
    it does not in any way participate in the interactions of sets and
    longest common prefix rules.

    .. code-block:: edgeql

        SELECT 1 IS int;
        # returns [True]

        SELECT User IS NOT SystemUser
        FILTER User.name = 'Alice';
        # returns [True]

        SELECT User IS (Text, Named);
        # returns [True, ..., True], one for every user


.. _ref_eql_expr_typecast:

Type Cast Expression
====================

A type cast expression converts the specified value to another value of
the specified type:

.. eql:synopsis::

    "<" <type> ">" <expression>

The *type* must be a scalar or a container type.

Type cast is a run-time operation.  The cast will succeed only if a
type conversion was defined for the type pair, and if the source value
satisfies the requirements of a target type.

EdgeDB allows casting any scalar

When a cast is applied to an expression of a known type, it represents a
run-time type conversion. The cast will succeed only if a suitable type
conversion operation has been defined.

Examples:

.. code-block:: edgeql

    # cast a string literal into an integer
    SELECT <int>"42";

    # cast an array of integers into an array of str
    SELECT <array<str>>[1, 2 , 3];

    # cast an issue number into a string
    SELECT <str>example::Issue.number;

Casts also work for converting tuples or declaring different tuple
element names for convenience.

.. code-block:: edgeql

    SELECT <tuple<int, str>>(1, 3);
    # returns [[1, '3']]

    WITH
        # a test tuple set, that could be a result of
        # some other computation
        stuff := (1, 'foo', 42)
    SELECT (
        # cast the tuple into something more convenient
        <tuple<a: int, name: str, b: int>>stuff
    ).name;  # access the 'name' element

An important use of *casting* is in defining the type of an empty
set ``{}``, which can be required for purposes of type disambiguation.

.. code-block:: edgeql

    WITH MODULE example
    SELECT Text {
        name :=
            Text[IS Issue].name IF Text IS Issue ELSE
            <str>{},
            # the cast to str is necessary here, because
            # the type of the computable must be defined
        body,
    };
