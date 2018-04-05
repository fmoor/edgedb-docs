.. _ref_edgeql_functions_random:


Random/UUID
===========

.. eql:function:: std::random() -> float64

    :return: pseudo-random number in the range `[0, 1)`
    :returntype: float64

    Return a pseudo-random number in the range `[0, 1)`.

.. eql:function:: std::uuid_generate_v1mc() -> uuid

    :return: version 1 UUID
    :returntype: uuid

    Return a version 1 UUID.

    The algorithm uses a random multicast MAC address instead of the
    real MAC address of the computer.
