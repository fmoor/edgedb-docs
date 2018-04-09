.. _ref_eql_statements_delete:

DELETE
======

.. eql:statement:: DELETE
    :haswith:

    ``DELETE`` -- remove objects from a database

    .. eql:synopsis::

        [ WITH <with-spec> [ , ... ] ]

        DELETE <expr>

    .. eql:clause:: WITH: WITH

        Alias declarations.

        The ``WITH`` clause allows specifying module aliases as well
        as expression aliases that can be referenced by the ``UPDATE``
        statement.  See :ref:`ref_eql_with` for more information.

    .. eql:clause:: DELETE: DELETE

        Remove objects returned by *expr* from the database.

        .. eql:synopsis::

            DELETE <expr>

    Output
    ~~~~~~

    On successful completion, a ``DELETE`` statement returns the set
    of deleted objects.


    Examples
    ~~~~~~~~

    Here's a simple example of deleting a specific user:

    .. code-block:: edgeql

        WITH MODULE example
        DELETE (SELECT User
                FILTER User.name = 'Alice Smith');
