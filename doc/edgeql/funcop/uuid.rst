.. _ref_eql_functions_uuid:

==============
UUID Functions
==============

.. eql:function:: std::uuid_generate_v1mc() -> uuid

    :return: version 1 UUID
    :returntype: uuid

    Return a version 1 UUID.

    The algorithm uses a random multicast MAC address instead of the
    real MAC address of the computer.
