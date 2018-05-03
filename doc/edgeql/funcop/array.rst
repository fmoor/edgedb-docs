.. _ref_eql_functions_array:


=====
Array
=====

:index: array

.. _ref_eql_expr_array_elref:

Array Element Reference
=======================

An element of an array can be referenced in the following form:

.. eql:synopsis::

    <expr> "[" <index-expr> "]"

Here, :eql:synopsis:`<expr>` is any expression of array type,
and :eql:synopsis:`<index-expr>` is any integer expression.

Example:

.. code-block:: edgeql-repl

    db> SELECT [1, 2, 3][0]
    {1}

Negative indexing is supported:

.. code-block:: edgeql-repl

    db> SELECT [1, 2, 3][-1]
    {3}

Referencing a non-existent array element will result in an empty set:

.. code-block:: edgeql-repl

    db> SELECT [1, 2, 3][0]
    {}


.. _ref_eql_expr_array_slice:

Array Slice
===========

An array slice can be referenced in the following form:

.. eql:synopsis::

    <expr> "[" <lower-bound> : <upper-bound> "]"

Here, :eql:synopsis:`<expr>` is any expression of array type,
and :eql:synopsis:`<lower-bound>` and
:eql:synopsis:`<upper-bound>` are arbitrary integer expressions.
Both :eql:synopsis:`<lower-bound>`, and
:eql:synopsis:`<upper-bound>` are optional.
An omitted :eql:synopsis:`<lower-bound>` default to zero,
and an omitted :eql:synopsis:`<upper-bound>` defaults to the
size of the array.  The upper bound is non-inclusive.

Examples:

.. code-block:: edgeql-repl

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

.. code-block:: edgeql-repl

    db> SELECT [1, 2, 3][10:20]
    {[]}


Functions
=========

.. eql:function:: std::array_agg(SET OF any) -> array<any>

    :param $0: input set
    :paramtype $0: SET OF any

    :return: array made of input set elements
    :returntype: array<any>

    :index: array aggregate

    Return the array made from all of the input set elements.

    The ordering of the input set will be preserved if specified.

    .. code-block:: edgeql

        SELECT array_agg({2, 3, 5});
        # returns [2, 3, 5]

        SELECT array_agg(User.name ORDER BY User.name);
        # returns a string array containing all User names sorted
        # alphabetically

.. eql:function:: std::array_contains(array<any>, any) -> bool

    :param $0: input array
    :paramtype $0: array<any>
    :param $1: element
    :paramtype $1: any

    :return: ``TRUE`` if the array contains the specified element
    :returntype: bool

    :index: array

    Return ``TRUE`` if the array contains the specified element.

    .. code-block:: edgeql

        SELECT array_contains([2, 3, 5], 2);
        # returns TRUE

        SELECT array_contains(['foo', 'bar'], 'baz');
        # returns FALSE

.. eql:function:: std::array_enumerate(array<any>) -> \
                  SET OF tuple<any, int64>

    :param $0: input array
    :paramtype $0: array<any>

    :return: set of tuples of the form ``(element, index)``
    :returntype: SET OF tuple<any, int64>

    :index: array enum

    Return a set of tuples of the form ``(element, index)``.

    Return a set of tuples where the first element is an array value
    and the second element is the index of that value for all values
    in the array.

    .. code-block:: edgeql

        SELECT array_enumerate([2, 3, 5]);
        # returns {(3, 1), (2, 0), (5, 2)}

    .. note::

        Notice that the ordering of the returned set is not
        guaranteed.

.. eql:function:: std::array_unpack(array<any>) -> SET OF any

    :param $0: input array
    :paramtype $0: array<any>

    :return: input array elements as a set
    :returntype: SET OF any

    :index: array set

    Return array elements as a set.

    The ordering of the returned set is not guaranteed.

    .. code-block:: edgeql

        SELECT array_unpack([2, 3, 5]);
        # returns {3, 2, 5}
