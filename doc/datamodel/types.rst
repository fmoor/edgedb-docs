.. _ref_edgedb_types:

Types
=====

EdgeDB types are divided into 3 groups: scalar types, object types and
collection types. Object types and collection types represent
different ways of structurally composing other types. Scalar types are
the most basic building blocks.

* `Scalar types`_

    The most basic types.

* `Object types`_

    Object types are used to semantically group data.

* `Collection types`_

    Collection types are used to package data based on usage. There
    are 4 kinds of collection types: :eql:type:`array`,
    :eql:type:`map`, :eql:type:`tuple`, and :eql:type:`json`.

* Meta-types_

    :eql:type:`SET-OF`, :eql:type:`OPTIONAL`, and :eql:type:`any`
    type annotations used for function signatures.


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


Collection types
----------------

Collection types represent various ways of packaging data. Typically
they do not represent any semantic relationship, but rather are used
for structural grouping. Often collection types are used to package
data in a certain way for serializing.

Creating collections syntactically (e.g. using ``[...]`` or ``(...)``)
is an element-wise operation. One way of thinking about these syntax
constructs is to treat them exactly like functions that simply turn
their arguments into a set of collections.

This means that the following code will create a set of tuples with
the first element being ``Issue`` and the second a :eql:type:`str`
representing the ``Issue.priority.name``:

.. code-block:: eql

    WITH MODULE example
    SELECT (Issue, Issue.priority.name);

Since ``priority`` is not a required link, not every ``Issue`` will
have one. It is important to realize that the above query will *only*
contain Issues with non-empty priorities. If it is desirable to have
*all* Issues, then coalescing (:eql:op:`??<COALESCE>`) or a
:ref:`shape<ref_edgeql_shapes>` query should be used instead.

On the other hand the following query will include *all* Issues,
because the tuple elements are made from the set of Issues and the set
produced by the aggregate function :eql:func:`array_agg`, which is
never ``{}``:

.. code-block:: eql

    WITH MODULE example
    SELECT (Issue, array_agg(Issue.priority.name));


.. eql:type:: std::array

    Arrays are homogeneous ordered collections.

    Array indexing starts at 0.

    At the moment only one-dimensional arrays are supported in EdgeDB.

    Array declaration must include the type of the elements. For
    example: :eql:type:`array\<int64\>`, :eql:type:`array\<User\>`, etc.

    Arrays support indexing and slicing operators:

    .. code-block:: eql

        SELECT [1, 2, 3];
        # this will return [[1, 2, 3]]

        WITH
            # define an array for testing
            arr := [1, 2, 3]
        SELECT
            # select the element at index 1
            arr[1];
        # this will return [2]

        WITH
            # define an array for testing
            arr := [1, 2, 3]
        SELECT
            # select the slice from
            # 1 (inclusive) to 3 (exclusive)
            arr[1:3];
        # this will return [2, 3]

    Another way of creating an array is to use :eql:func:`array_agg`
    built-in, which converts a set into an array. If the ordering is
    important the ``ORDER`` clause must be specified for the set,
    otherwise no specific ordering guarantee can be made for the
    :eql:func:`array_agg` aggregate function:

    .. code-block:: eql

        WITH MODULE example
        SELECT array_agg(
            (SELECT User ORDER BY User.name)
        );


.. eql:type:: std::map

    Maps are indexed homogeneous collections.

    Map declaration must include the types of keys and values. For
    example: :eql:type:`map\<int, str\>`, :eql:type:`map\<str, User\>`, etc.

    Maps are indexed homogeneous collections, where the indexes are
    arbitrary but must be all of the same type.  Values don't have to
    be the same type as indexes, but they must still be the same type
    as each other.

    No specific ordering of a map is assumed or guaranteed, thus
    slicing operators are not available for them.

    Examples of map usage:

    .. code-block:: eql

        SELECT ['a' -> 1, 'b' -> 2, 'c' -> 3];
        # this will return [{'a': 1, 'b': 2, 'c': 3}]

        WITH
            # define a map for testing
            map := ['a' -> 1, 'b' -> 2, 'c' -> 3]
        SELECT
            # select the element at index 'b'
            map['b'];
        # this will return [2]


.. eql:type:: std::tuple

    Tuples are ordered heterogeneous collections.

    Their components are ordered and can be of any type. Two tuples
    are equal if all of their components are equal and in the same
    order.

    Tuple type declaration must include the types of their components.
    For example: :eql:type:`tuple\<int, int\>`,
    :eql:type:`tuple\<int, int, str\>`, :eql:type:`tuple\<str, User\>`,
    :eql:type:`tuple\<bool, tuple\<User, int\>\>`, etc.

    Examples of map usage:

    .. code-block:: eql

        # a simple 2-tuple made of a str and int
        SELECT ('foo', 42);

        WITH
            # define a tuple for testing
            tup := ('foo', 42)
        SELECT
            # select the first element of the tuple
            tup.0;
        # returns ['foo']

        WITH
            tup := ('foo', 42)
        SELECT
            # create a new 2-tuple reversing the elements
            (tup.1, tup.0);
        # returns [[42, 'foo']]

        WITH
            tup := ('foo', 42)
        SELECT
            # compare 2 tuples
            tup = ('foo', 42);
        # returns [True]


    Tuple elements can be *named*, however names do not affect
    the ordering of elements within the tuple in any way.

    The names are used for convenience making it easier to refer
    to different elements as well as in tuple serialization.

    Only valid identifiers can be used to name tuple elements.

    .. code-block:: eql

        # a simple named 2-tuple made of a str and int
        SELECT (a := 'foo', b := 42);

        WITH
            # define a tuple for testing
            tup := (a := 'foo', b := 42)
        SELECT
            # select the element of the tuple denoted by 'a'
            tup.a;
        # returns ['foo']

        WITH
            tup := (a := 'foo', b := 42)
        SELECT
            # compare 2 tuples
            tup = ('foo', 42);
        # returns [True]

        WITH
            tup := (a := 'foo', b := 42)
        SELECT
            # compare 2 tuples
            tup = (b := 42, a := 'foo');
        # returns [False] because the ordering of
        # the tuple elements is different

        WITH
            tup1 := (a := 'foo', b := 42),
            tup2 := (b := 42, a := 'foo')
        SELECT
            # compare tuple elements
            (tup1.a = tup2.a, tup1.b = tup1.b);
        # returns [[True, True]]

    It is possible to nest other collection types and tuples within
    each other:

    .. code-block:: eql

        # array of 3-tuples
        SELECT [
            # where each tuple has:
            (
                # str,
                'foo',
                # array of int,
                [1, 2],
                # tuple (int, int) as elements
                (3, 5),
            ),
            (
                'bar',
                [100, 200, 9001],
                (-2, 4),
            ),
        ];


.. eql:type:: std::json

    JSON (JavaScript Object Notation) data.

    JSON type allows storing structured, but unvalidated data. Unlike
    other collection types this type does not require declaring the
    internal structure. As such, no specific guaranteed about JSON data
    can be given.


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
