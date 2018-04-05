.. _ref_edgeql_functions_array:


Array
=====

.. eql:function:: std::array_agg(SET OF any) -> array<any>

    :param $0: input set
    :paramtype $0: SET OF any

    :return: array made of input set elements
    :returntype: array<any>

    Return the array made from all of the input set elements.

    The ordering of the input set will be preserved if specified.

    .. code-block:: eql

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

    Return ``TRUE`` if the array contains the specified element.

    .. code-block:: eql

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

    Return a set of tuples of the form ``(element, index)``.

    Return a set of tuples where the first element is an array value
    and the second element is the index of that value for all values
    in the array.

    .. code-block:: eql

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

    Return array elements as a set.

    The ordering of the returned set is not guaranteed.

    .. code-block:: eql

        SELECT array_unpack([2, 3, 5]);
        # returns {3, 2, 5}
