.. _ref_eql_funcop_math:

======================
Mathematical Operators
======================

This section describes mathematical operators
provided by EdgeDB.

.. eql:operator:: PLUS: A + B

    :optype A: numeric
    :optype B: numeric
    :resulttype: numeric

    Arithmetic addition.


.. eql:operator:: MINUS: A - B

    :optype A: numeric
    :optype B: numeric
    :resulttype: numeric

    Arithmetic subtraction.


.. eql:operator:: UMINUS: -A

    :optype A: numeric
    :resulttype: numeric

    Arithmetic negation.


.. eql:operator:: MULT: A * B

    :optype A: numeric
    :optype B: numeric
    :resulttype: numeric

    Arithmetic multiplication.


.. eql:operator:: DIV: A / B

    :optype A: numeric
    :optype B: numeric
    :resulttype: numeric

    Arithmetic division.


.. eql:operator:: MOD: A % B

    :optype A: numeric
    :optype B: numeric
    :resulttype: numeric

    Remainder from division (modulo).


.. eql:operator:: POW: A ^ B

    :optype A: numeric
    :optype B: numeric
    :resulttype: numeric

    Power operation.
