.. _ref_edgeql_functions_setagg:


Aggregates
==========

.. eql:function:: std::count(SET OF any) -> int

    :param $0: input set
    :paramtype $0: SET OF any

    :return: number of elements in the input set
    :returntype: int64

    Return the number of elements in a set.

    .. code-block:: eql

        SELECT count({2, 3, 5});
        # returns 3

        SELECT count(User);
        # returns the number of User objects in the DB

.. eql:function:: std::sum(SET OF numeric) -> numeric

    :param $0: input set
    :paramtype $0: SET OF numeric

    :return: sum of the input set of numbers
    :returntype: numeric

    Return the sum of the set of numbers.

    The numbers have to be either :eql:type:`numeric` or any type that
    can be cast into it, such as :eql:type:`float64` or
    :eql:type:`int64`.

    .. code-block:: eql

        SELECT sum({2, 3, 5});
        # returns 10

        SELECT sum({0.2, 0.3, 0.5});
        # returns 1.0

Here's a list of aggregate functions covered in other sections:

* :eql:func:`array_agg`
