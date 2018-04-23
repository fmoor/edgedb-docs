.. _ref_eql_funcop_conditional:

=======================
Conditional Expressions
=======================

This section describes conditional expressions provided by EdgeDB.


IF..ELSE
========

.. eql:operator:: IF..ELSE: A IF C ELSE B

    :optype A: SET OF any
    :optype C: bool
    :optype B: SET OF any
    :resulttype: SET OF any

    Conditionally provide one or the other result.

    IF *C* is ``true``, then the value of the ``IF..ELSE`` expression
    is the value of *A*, if *C* is ``false``, the result is the value of
    *B*.

    ``IF..ELSE`` expressions can be chained when checking multiple conditions
    is necessary:

    .. code-block:: edgeql

        SELECT 'Apple' IF Fruit IS Apple ELSE
               'Banana' IF Fruit IS Banana ELSE
               'Orange' IF Fruit IS Orange ELSE
               'Other';


COALESCE
========

.. eql:operator:: COALESCE: A ?? B

    :optype A: OPTIONAL any
    :optype B: SET OF any
    :resulttype: SET OF any

    Evaluate to ``A`` for non-empty ``A``, otherwise evaluate to ``B``.

    A typical use case of coalescing operator is to provide default
    values for optional properties.

    .. code-block:: edgeql

        # Get a set of tuples (<issue name>, <priority>)
        # for all issues.
        SELECT (Issue.name, Issue.priority.name ?? 'n/a');

    Without the coalescing operator the above query would skip any
    ``Issue`` without priority.
