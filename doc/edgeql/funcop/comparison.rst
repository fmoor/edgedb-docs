.. _ref_eql_funcop_comparison:

====================
Comparison Operators
====================

EdgeDB supports the following comparison operators:

.. eql:operator:: EQ: A = B

    :optype A: any
    :optype B: any
    :resulttype: bool

    Compare two values for equality.


.. eql:operator:: NEQ: A != B

    :optype A: any
    :optype B: any
    :resulttype: bool

    Compare two values for inequality.


.. eql:operator:: COALEQ: A ?= B

    :optype A: OPTIONAL any
    :optype B: OPTIONAL any
    :resulttype: bool

    Compare two values for equality.

    Works the same as regular :eql:op:`=<EQ>`, but also allows
    comparing ``{}``.  Two ``{}`` are considered equal.


.. eql:operator:: COALNEQ: A ?!= B

    :optype A: OPTIONAL any
    :optype B: OPTIONAL any
    :resulttype: bool

    Compare two values for inequality.

    Works the same as regular :eql:op:`\!=<NEQ>`, but also allows
    comparing ``{}``.  Two ``{}`` are considered equal.


.. eql:operator:: LT: A < B

    :optype A: any
    :optype B: any
    :resulttype: bool

    ``TRUE`` if ``A`` is less than ``B``.


.. eql:operator:: GT: A > B

    :optype A: any
    :optype B: any
    :resulttype: bool

    ``TRUE`` if ``A`` is greater than ``B``.


.. eql:operator:: LTEQ: A <= B

    :optype A: any
    :optype B: any
    :resulttype: bool

    ``TRUE`` if ``A`` is less than or equal to ``B``.


.. eql:operator:: GTEQ: A >= B

    :optype A: any
    :optype B: any
    :resulttype: bool

    ``TRUE`` if ``A`` is greater than or equal to ``B``.


.. eql:operator:: EXISTS: EXISTS A

    :optype A: SET OF any
    :resulttype: bool

    Test whether a set is not empty.

    ``EXISTS`` is an aggregate operator that returns a singleton set
    ``{true}`` if the input set is not empty and returns ``{false}``
    otherwise.
