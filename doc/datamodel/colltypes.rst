.. _ref_datamodel_collection_types:

Collection types
================

Collection types are special generic types used to group homogeneous or
heterogeneous data.


.. eql:type:: std::tuple

    A tuple type is a heterogeneous sequence of other types.

    Tuple elements can optionally have names,
    in which case the tuple is called a *named tuple*.

    A tuple type can be explicitly declared in an expression or schema
    declaration using the following syntax:

    .. code-block:: pseudo-eql

        tuple<[element_type, ...]>

    A named tuple:

    .. code-block:: pseudo-eql

        tuple<element_name := element_type [, ... ]>

    Any type can be used as a tuple element type.

    A tuple type is created implicitly when a
    :ref:`tuple constructor <ref_eql_expr_tuple_ctor>` is
    used:

    .. code-block:: pseudo-eql

        # a simple 2-tuple made of a str and int
        db> SELECT ('foo', 42).__type__.name;
        {"std::tuple<std::str, std::int64>"}

    Two tuples are equal if all of their elements are equal and in the same
    order.  Note that element names in named tuples are not significant for
    comparison:

    .. code-block:: pseudo-eql

        db> SELECT (1, 2, 3) = (a := 1, b := 2, c := 3);
        {True}


.. eql:type:: std::array

    Arrays represent a one-dimensional homogeneous ordered list.

    Array indexing starts at 0.

    A tuple type can be explicitly declared in an expression or schema
    declaration using the following syntax:

    .. code-block:: pseudo-eql

        array<element_type>

    With the exception of other array types, any type can be used as an
    array element type.

    An array type is created implicitly when an
    :ref:`array constructor <ref_eql_expr_array_ctor>` is
    used:

    .. code-block:: pseudo-eql

        db> SELECT [1, 2].__type__;
        {"std::array<std::int64>"}


.. eql:type:: std::map

    Maps are homogeneous key-value types.

    A map type can be explicitly declared in an expression or schema
    declaration using the following syntax:

    .. code-block:: pseudo-eql

        map<key_type, element_type>

    Any type can be used as a map key type or a map element type.

    No specific ordering of a map is assumed or guaranteed.
