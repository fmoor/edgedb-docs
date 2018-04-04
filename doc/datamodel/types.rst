.. _ref_edgedb_types:

Types
=====

There are two main categories of types in EdgeDB: *object types* and
*primitive types*.  Primitive types are further subdivided into
*scalar types* and *collection types*.

* `Object types`_

    A collection of links to other types.

* `Scalar types`_

    Individual basic types such as :eql:type:`int32` and :eql:type:`str`.

* `Collection types`_

    There are 3 kinds of collection types built into EdgeDB:
    :eql:type:`array`, :eql:type:`map`, and :eql:type:`tuple`.

* Meta-types_

    :eql:type:`SET-OF`, :eql:type:`OPTIONAL`, and :eql:type:`any`
    type annotations used for function signatures.


Object types
------------

.. eql:type:: std::Object

    Base type which every object type implicitly extends.

    Object types represent relationships between types. They use
    ``links`` to semantically group other data types.

    For example:

    .. code-block:: eschema

        concept User:
            required link name to str
            link email to str

    The above example defines an object type ``User``. This type has
    two links: ``name`` and ``email``. Both of the links are
    :eql:type:`strings<str>`. Link ``name`` is *required*, whereas
    ``email`` is *optional*.

    Object types make up the core of EdgeDB. Various queries allow to
    retrieve the data stored in EdgeDB by exploring the relationships
    defined as object types. Collectively the object types define the
    semantic structure of the data in EdgeDB.


Scalar types
------------

Scalar types are the most basic types. Instances are collectively
known as *scalars*.

.. eql:type:: std::numeric

    Any number of arbitrary precision.

    All of the following types can be cast into numeric:
    :eql:type:`int16`, :eql:type:`int32`, :eql:type:`int64`,
    :eql:type:`float32`, and :eql:type:`float64`.

.. eql:type:: std::int16

    A 16-bit signed integer.

.. eql:type:: std::int32

    A 32-bit signed integer.

.. eql:type:: std::int64

    A 64-bit signed integer.

.. eql:type:: std::float32

    A variable precision, inexact number.

    Minimal guaranteed precision is at least 6 decimal digits.

.. eql:type:: std::float64

    A variable precision, inexact number.

    Minimal guaranteed precision is at least 15 decimal digits.

.. eql:type:: std::bool

    A boolean type with possible values of ``TRUE`` and ``FALSE``.

.. eql:type:: std::bytes

    A sequence of bytes.

.. eql:type:: std::str

    A unicode string of text.

.. eql:type:: std::uuid

    Universally Unique Identifiers (UUID).

    For formal definition see RFC 4122 and ISO/IEC 9834-8:2005.

.. eql:type:: std::datetime

    A type representing date, time, and time zone.

.. eql:type:: std::date

    A type representing date and time zone.

.. eql:type:: std::time

    A type representing time and time zone.

.. eql:type:: std::timedelta

    A type representing a relative time interval.

    The time interval can be specified in terms of microseconds,
    milliseconds, seconds, minutes, hours, days, weeks, months, years,
    decades, centuries, millennia, e.g.:

    .. code-block:: eql

        SELECT <timedelta>'2.3 millennia 3 weeks';

.. eql:type:: std::sequence

    Auto-incrementing sequence of :eql:type:`int64`.

.. eql:type:: std::json

    Arbitrary JSON data.


Collection types
----------------

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
    :ref:`tuple constructor <ref_edgeql_expressions_tuple_constructor>` is
    used:

    .. code-block:: pseudo-eql

        # a simple 2-tuple made of a str and int
        db> SELECT ('foo', 42).__type__;
        std::tuple<std::str, std::int64>

    Two tuples are equal if all of their elements are equal and in the same
    order.  Note that element names in named tuples are not significant for
    comparison:

    .. code-block:: pseudo-eql

        db> SELECT (1, 2, 3) = (a := 1, b := 2, c := 3);
        True


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
    :ref:`array constructor <ref_edgeql_expressions_array_constructor>` is
    used:

    .. code-block:: pseudo-eql

        db> SELECT [1, 2].__type__;
        std::array<std::int64>


.. eql:type:: std::map

    Maps are homogeneous key-value types.

    A map type can be explicitly declared in an expression or schema
    declaration using the following syntax:

    .. code-block:: pseudo-eql

        map<key_type, element_type>

    Any type can be used as a map key type or a map element type.

    No specific ordering of a map is assumed or guaranteed.


Meta-types
----------

There are some additional concepts related to typing that come up in
function signatures. See :ref:`parameter types
<ref_edgeql_fundamentals_function>` for more details.


.. eql:type:: SET-OF

    Denotes that the argument must be treated a whole set.


.. eql:type:: OPTIONAL

    Denotes an element-wise argument that has special handling if
    missing.

    If the argument is an empty set the function will still be
    called with an ``{}`` (empty set) value.


.. eql:type:: std::any

    Pseudo-type denoting that the argument can be of any type.
