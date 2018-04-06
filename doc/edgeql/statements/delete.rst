.. _ref_eql_statements_delete:

Delete
------

``DELETE`` statement removes the specified set of objects from the
database. Therefore, a ``FILTER`` can be applied to the set being
removed, while the ``DELETE`` statement itself does not have a
``FILTER`` clause. Just like ``INSERT`` if used as an expression it
will return the set of removed objects.

The data flow of a ``DELETE`` block can be conceptualized like this:

.. eql:statement:: DELETE
    :haswith:

    ``DELETE`` -- remove objects from a database

    .. eql:synopsis::

        [ WITH module_aliases, expression_aliases ]

        DELETE
            <expr>  # delete the following objects

    Notice that there are no other clauses in the ``DELETE`` statement.
    This is because it is a mutation statement and not typically used to
    query the DB.

Here's a simple example of deleting a specific user:

.. code-block:: edgeql

    WITH MODULE example
    DELETE (SELECT User
            FILTER User.name = 'Alice Smith');
