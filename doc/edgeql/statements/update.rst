.. _ref_eql_statements_update:

Update
------

It is possible to update already existing objects via ``UPDATE``
statement. An update can target a single object or be a bulk update.
If used as an expression, it will return the set of objects on which
it operated.

The data flow of an ``UPDATE`` block can be conceptualized like this:

.. eql:statement:: UPDATE
    :haswith:

    ``UPDATE`` -- update objects in a database

    .. eql:synopsis::

        [ WITH MODULE module_aliases, expression_aliases ]

        UPDATE
            <expr>  # compute a set of things

        # optional clause
        FILTER
            <expr>  # filter the computed set

        SET
            <shape> # update objects based on the
                    # computed/filtered set

Notice that there are no ``ORDER``, ``OFFSET`` or ``LIMIT`` clauses in
the ``UPDATE`` statement. This is because it is a mutation statement
and not typically used to query the DB.

Here are a couple of examples of using the ``UPDATE`` statement:

.. code-block:: edgeql

    # update the user with the name 'Alice Smith'
    WITH MODULE example
    UPDATE User
    FILTER User.name = 'Alice Smith'
    SET {
        name := 'Alice J. Smith'
    };

    # update all users whose name is 'Bob'
    WITH MODULE example
    UPDATE User
    FILTER User.name LIKE 'Bob%'
    SET {
        name := User.name + '*'
    };

The statement ``FOR <x> IN <expr>`` allows to express certain bulk
updates more clearly. See
:ref:`Usage of FOR statement<ref_eql_forstatement>` for more details.


Clause signatures
+++++++++++++++++

Here is a summary of clauses that can be used with ``UPDATE``:

- *A* FILTER ``SET OF`` *B*
- *A* SET  ``SET OF`` *B1*, ..., ``SET OF`` *Bn*
