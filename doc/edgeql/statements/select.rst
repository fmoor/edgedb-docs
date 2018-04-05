.. _ref_edgeql_statements_select:

Select
======

.. eql:statement:: SELECT
    :haswith:

    A ``SELECT`` statement returns a set of objects.

    .. eql:synopsis::

        [ WITH module_aliases, expression_aliases ]

        SELECT <expr>

        [ FILTER <expr> ]

        [ ORDER BY <expr> [direction] [THEN ...] ]

        [ OFFSET <expr> ]

        [ LIMIT  <expr> ]

    The first clause is ``SELECT``. It indicates that ``FILTER``, ``ORDER
    BY``, ``OFFSET``, or ``LIMIT`` clauses may follow an expression, i.e.
    it makes an expression into a ``SELECT`` statement. Without any of the
    optional clauses a ``(SELECT Expr)`` is completely equivalent to
    ``Expr`` for any expression ``Expr``.

    .. eql:clause:: FILTER: A FILTER B

        :paramtype A: any
        :paramtype B: SET OF any
        :returntype: any

        The ``FILTER`` clause ...

        The ``FILTER`` clause cannot affect anything aggregate-like in the
        preceding ``SELECT`` clause. This is due to how ``FILTER`` clause
        works. It can be conceptualized as a function like ``filter($input,
        SET OF $cond)``, where the ``$input`` represents the value of the
        preceding clause, while the ``$cond`` represents the filtering
        condition expression. Consider the following:

        .. code-block:: eql

            WITH MODULE example
            SELECT count(User)
            FILTER User.name LIKE 'Alice%';


See also :eql:stmt:`SELECT`.
See also :eql:clause:`FILTER <SELECT:FILTER>`.


A ``SELECT`` statement returns a set of objects. The data flow of a
``SELECT`` block can be conceptualized like this:

.. code-block:: pseudo-eql

    WITH MODULE example

    # select clause
    SELECT
        <expr>  # compute a set of things

    # optional clause
    FILTER
        <expr>  # filter the computed set

    # optional clause
    ORDER BY
        <expr>  # define ordering of the filtered set

    # optional clause
    OFFSET
        <expr>  # slice the filtered/ordered set

    # optional clause
    LIMIT
        <expr>  # slice the filtered/ordered set

Please note that the ``ORDER BY`` clause defines ordering that can
only be relied upon if the resulting set is not used in any other
operation. ``SELECT``, ``OFFSET`` and ``LIMIT`` clauses are the only
exception to that rule as they preserve the inherent ordering of the
underlying set.

The first clause is ``SELECT``. It indicates that ``FILTER``, ``ORDER
BY``, ``OFFSET``, or ``LIMIT`` clauses may follow an expression, i.e.
it makes an expression into a ``SELECT`` statement. Without any of the
optional clauses a ``(SELECT Expr)`` is completely equivalent to
``Expr`` for any expression ``Expr``.

Consider an example using the ``FILTER`` optional clause:

.. code-block:: eql

    WITH MODULE example
    SELECT User {
        name,
        owned := (SELECT
            User.<owner[IS Issue] {
                number,
                body
            }
        )
    }
    FILTER User.name LIKE 'Alice%';

The above example retrieves a single user with a specific name. The
fact that there is only one such user is a detail that can be well-
known and important to the creator of the DB, but otherwise non-
obvious. However, forcing the cardinality to be at most 1 by using the
``LIMIT`` clause ensures that a set with a single object or
``{}`` is returned. This way any further code that relies on the
result of this query can safely assume there's only one result
available.

.. code-block:: eql

    WITH MODULE example
    SELECT User {
        name,
        owned := (SELECT
            User.<owner[IS Issue] {
                number,
                body
            }
        )
    }
    FILTER User.name LIKE 'Alice%'
    LIMIT 1;

Next example makes use of ``ORDER BY`` and ``LIMIT`` clauses:

.. code-block:: eql

    WITH MODULE example
    SELECT Issue {
        number,
        body,
        due_date
    }
    FILTER
        EXISTS Issue.due_date
        AND
        Issue.status.name = 'Open'
    ORDER BY
        Issue.due_date
    LIMIT 3;

The above query retrieves the top 3 open Issues with the closest due
date.


Filter
++++++

The ``FILTER`` clause cannot affect anything aggregate-like in the
preceding ``SELECT`` clause. This is due to how ``FILTER`` clause
works. It can be conceptualized as a function like ``filter($input,
SET OF $cond)``, where the ``$input`` represents the value of the
preceding clause, while the ``$cond`` represents the filtering
condition expression. Consider the following:

.. code-block:: eql

    WITH MODULE example
    SELECT count(User)
    FILTER User.name LIKE 'Alice%';

The above can be conceptualized as:

.. code-block:: eql

    WITH MODULE example
    SELECT _filter(
        count(User),
        User.name LIKE 'Alice%'
    );

In this form it is more apparent that ``User`` is a ``SET OF``
argument (of :eql:func:`count`), while ``User.name LIKE 'Alice%'`` is
also a ``SET OF`` argument (of ``filter``). So the symbol ``User`` in
these two expressions exists in 2 parallel scopes. Contrast it with:

.. code-block:: eql

    # This will actually only count users whose name starts with
    # 'Alice'.

    WITH MODULE example
    SELECT count(
        (SELECT User
         FILTER User.name LIKE 'Alice%')
    );

    # which can be represented as:
    WITH MODULE example
    SELECT count(
        _filter(User,
               User.name LIKE 'Alice%')
    );

Clause signatures
+++++++++++++++++

Here is a summary of clauses that can be used with ``SELECT``:

- *A* FILTER ``SET OF`` *B*
- *A* ORDER BY ``SET OF`` *B*
- ``SET OF`` *A* OFFSET ``SET OF`` *B*
- ``SET OF`` *A* LIMIT ``SET OF`` *B*
