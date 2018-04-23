.. _ref_eql_funcop_set:

=============
Set Operators
=============

This section describes EdgeQL operators that work on whole sets.


DISTINCT
========

.. eql:operator:: DISTINCT: DISTINCT A

    :optype A: SET OF any
    :resulttype: any

    Return a set without repeating any elements.

    ``DISTINCT`` is a set operator that returns a new set where
    no member is equal to any other member.


IN
==

.. eql:operator:: IN: A IN B or A NOT IN B

    :optype A: any
    :optype B: SET OF any
    :resulttype: bool

    Test the membership of an element in a set.

    Set membership operators :eql:op:`IN` and :eql:op:`NOT IN<IN>`
    that test for each element of ``A`` whether it is present in ``B``.

    .. code-block:: edgeql

        SELECT 1 IN {1, 3, 5};
        # returns [True]

        SELECT 'Alice' IN User.name;

        SELECT {1, 2} IN {1, 3, 5};
        # returns [True, False]


UNION
=====

.. eql:operator:: UNION: A UNION B

    :optype A: SET OF any
    :optype B: SET OF any
    :resulttype: SET OF any

    Merge two sets.

    Since EdgeDB sets are formally multisets, ``UNION`` is a *multiset sum*,
    so effectively it merges two multisets keeping all of their members.

    For example, applying ``UNION`` to ``{1, 2, 2}`` and
    ``{2}``, results in ``{1, 2, 2, 2}``.

    If you need a distinct union, wrap it with :eql:op:`DISTINCT`.
