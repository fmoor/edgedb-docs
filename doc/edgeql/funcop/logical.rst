.. _ref_eql_funcop_logical:

=================
Logical Operators
=================

EdgeDB supports the following boolean logical operators:
``AND``, ``OR``, and ``NOT``.

.. eql:operator:: OR: A OR B

    :optype A: bool
    :optype B: bool
    :resulttype: bool

    Logical disjunction.


.. eql:operator:: AND: A AND B

    :optype A: bool
    :optype B: bool
    :resulttype: bool

    Logical conjunction.


.. eql:operator:: NOT: NOT A

    :optype A: bool
    :resulttype: bool

    Logical negation.


The ``AND`` and ``OR`` operators are commutative.

The truth tables are as follows:

+-------+-------+-----------+----------+
|   a   |   b   |  a AND b  |  a OR b  |
+=======+=======+===========+==========+
| TRUE  | TRUE  |   TRUE    |   TRUE   |
+-------+-------+-----------+----------+
| TRUE  | FALSE |   FALSE   |   TRUE   |
+-------+-------+-----------+----------+
| FALSE | TRUE  |   FALSE   |   TRUE   |
+-------+-------+-----------+----------+
| FALSE | FALSE |   FALSE   |   FALSE  |
+-------+-------+-----------+----------+

+-------+---------+
|   a   |  NOT a  |
+=======+=========+
| TRUE  |  FALSE  |
+-------+---------+
| FALSE |  TRUE   |
+-------+---------+
