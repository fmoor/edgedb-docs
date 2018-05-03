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
    :index: plus add

    Arithmetic addition.


.. eql:operator:: MINUS: A - B

    :optype A: numeric
    :optype B: numeric
    :resulttype: numeric
    :index: minus subtract

    Arithmetic subtraction.


.. eql:operator:: UMINUS: -A

    :optype A: numeric
    :resulttype: numeric
    :index: unary minus subtract

    Arithmetic negation.


.. eql:operator:: MULT: A * B

    :optype A: numeric
    :optype B: numeric
    :resulttype: numeric
    :index: multiply multiplication

    Arithmetic multiplication.


.. eql:operator:: DIV: A / B

    :optype A: numeric
    :optype B: numeric
    :resulttype: numeric
    :index: divide division

    Arithmetic division.


.. eql:operator:: MOD: A % B

    :optype A: numeric
    :optype B: numeric
    :resulttype: numeric
    :index: modulo mod division

    Remainder from division (modulo).


.. eql:operator:: POW: A ^ B

    :optype A: numeric
    :optype B: numeric
    :resulttype: numeric
    :index: power pow

    Power operation.
